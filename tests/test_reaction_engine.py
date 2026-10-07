import pytest

from atomos_perdidos.core.reaction_engine import balance_equation


@pytest.mark.parametrize(
    ("reactants", "products", "expected"),
    [
        (["H2", "O2"], ["H2O"], "2H2 + O2 → 2H2O"),
        (["CH4", "O2"], ["CO2", "H2O"], "CH4 + 2O2 → CO2 + 2H2O"),
        (["Fe", "O2"], ["Fe2O3"], "4Fe + 3O2 → 2Fe2O3"),
        (["Na", "Cl2"], ["NaCl"], "2Na + Cl2 → 2NaCl"),
    ],
)
def test_balance_common_reactions(reactants, products, expected):
    result = balance_equation(reactants, products)
    assert result["equation"] == expected
    assert result["conserved"] is True


def test_requires_both_sides():
    with pytest.raises(ValueError):
        balance_equation(["H2"], [])


def test_reaction_quantities_finds_limiting_reagent():
    from atomos_perdidos.core.reaction_engine import reaction_quantities
    result = reaction_quantities(["H2", "O2"], ["H2O"], [5, 1])
    assert result["limiting_reagent"] == "O2"
    assert result["products"][0]["theoretical_moles"] == 2.0
    assert result["reactants"][0]["remaining_moles"] == 3.0


def test_reaction_optimization_rewards_balanced_resources():
    from atomos_perdidos.lab.experiment_engine import optimize_reaction
    result = optimize_reaction("rendimiento_reaccion", {"resources": {"H2": 2, "O2": 1}})
    assert result["limiting_reagent"] == "H2"
    assert result["efficiency"] == 100.0
    assert result["score"] >= 90
    assert result["reward"]["rank"] == "maestro"


def test_reaction_optimization_penalizes_bad_ratio():
    from atomos_perdidos.lab.experiment_engine import optimize_reaction
    result = optimize_reaction("rendimiento_reaccion", {"resources": {"H2": 1, "O2": 5}})
    assert result["efficiency"] < 100
    assert result["excess_reagents"] == ["O2"]
