from experiment_engine import get_experiment, list_experiments, run_experiment


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
        },
    )
    assert result["score"] == 60


def test_unknown_experiment():
    assert get_experiment("does-not-exist") is None
