from atomos_perdidos.lab.experiment_engine import get_experiment, list_experiments, run_experiment


def test_experiment_catalog_is_available():
    experiments = list_experiments()
    assert len(experiments) >= 3
    assert all("prediction_options" in item for item in experiments)


def test_polarity_experiment_scores_correct_prediction():
    result = run_experiment(
        "polaridad_agua",
        {
            "prediction": "polar",
            "observations": ["La molécula es angular."],
            "atoms": [
                {"id": "o", "symbol": "O"},
                {"id": "h1", "symbol": "H"},
                {"id": "h2", "symbol": "H"},
            ],
            "bonds": [
                {"a": "o", "b": "h1", "order": 1},
                {"a": "o", "b": "h2", "order": 1},
            ],
        },
    )
    assert result["completed"]
    assert result["score"] == 100
    assert result["result"]["polar"] is True


def test_conservation_experiment_balances_water():
    result = run_experiment(
        "conservacion_materia",
        {
            "prediction": "se_conserva",
            "observations": ["Los átomos se conservan."],
            "equation": {"reactants": ["H2", "O2"], "products": ["H2O"]},
        },
    )
    assert result["completed"]
    assert result["score"] == 100
    assert result["result"]["equation"] == "2H2 + O2 → 2H2O"


def test_molar_mass_experiment_identifies_co2_as_heavier():
    result = run_experiment(
        "masa_molar",
        {
            "prediction": "segunda_mayor",
            "observations": ["CO2 tiene mayor masa molar."],
            "formulas": ["H₂O", "CO₂"],
            "variables": {"first_amount": 1, "second_amount": 1},
        },
    )
    assert result["completed"]
    assert result["score"] == 100
    assert result["result"]["greater"] == "second"


def test_observation_is_required_for_full_score():
    result = run_experiment(
        "masa_molar",
        {
            "prediction": "segunda_mayor",
            "formulas": ["H₂O", "CO₂"],
            "variables": {"first_amount": 1, "second_amount": 1},
        },
    )
    assert result["score"] == 80


def test_unknown_experiment():
    assert get_experiment("does-not-exist") is None


def test_molar_mass_experiment_responds_to_quantity_variables():
    result = run_experiment(
        "masa_molar",
        {
            "prediction": "segunda_mayor",
            "observations": ["La cantidad cambia la masa total."],
            "variables": {"first_amount": 1, "second_amount": 1},
        },
    )
    assert result["result"]["greater"] == "second"
    assert result["result"]["total_masses"]["CO₂"] > result["result"]["total_masses"]["H₂O"]


def test_experiment_rejects_out_of_range_variable():
    import pytest
    with pytest.raises(ValueError):
        run_experiment(
            "conservacion_materia",
            {"variables": {"reactant_amount": 99}},
        )


def test_limiting_reagent_experiment_uses_actual_quantities():
    result = run_experiment(
        "rendimiento_reaccion",
        {
            "prediction": "reactivo_2",
            "observations": ["O2 se agota primero."],
            "variables": {"first_moles": 10, "second_moles": 1},
        },
    )
    assert result["completed"]
    assert result["result"]["limiting_reagent"] == "O2"
    assert result["score"] == 100
    assert result["result"]["products"][0]["theoretical_moles"] == 2.0


def test_limiting_reagent_reports_excess():
    result = run_experiment(
        "rendimiento_reaccion",
        {
            "prediction": "reactivo_1",
            "variables": {"first_moles": 2, "second_moles": 2},
        },
    )
    assert result["result"]["limiting_reagent"] == "H2"
    assert result["result"]["excess_reagents"] == ["O2"]
