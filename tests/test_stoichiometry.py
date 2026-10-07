import pytest

from stoichiometry import analyze_formula_stoichiometry, molar_mass, parse_formula


def test_parse_formula():
    assert parse_formula("H₂O") == {"H": 2, "O": 1}
    assert parse_formula("CO2") == {"C": 1, "O": 2}


def test_water_molar_mass():
    assert molar_mass("H2O") == pytest.approx(18.015, abs=0.002)


def test_carbon_dioxide_molar_mass():
    assert molar_mass("CO2") == pytest.approx(44.009, abs=0.002)


def test_mass_percentages_sum_to_100():
    result = analyze_formula_stoichiometry("H2O")
    assert sum(result["mass_percentages"].values()) == pytest.approx(100, abs=0.001)


def test_parentheses_are_explicitly_not_supported_yet():
    with pytest.raises(ValueError):
        parse_formula("Ca(OH)2")
