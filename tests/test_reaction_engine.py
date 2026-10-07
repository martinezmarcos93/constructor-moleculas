import pytest

from reaction_engine import balance_equation


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
