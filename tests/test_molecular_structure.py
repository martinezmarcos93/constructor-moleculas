from molecular_structure import MoleculeStructure
from vsepr import classify_vsepr


def make(*atoms):
    s = MoleculeStructure()
    for i, symbol in enumerate(atoms):
        s.add_atom(str(i), symbol)
    return s


def test_water_structure():
    s = make("O", "H", "H")
    s.add_bond("0", "1", 1).add_bond("0", "2", 1)
    assert s.formula() == "H₂O"
    assert s.is_valid()
    result = classify_vsepr(s)
    assert result["geometry"] == "angular"
    assert result["lone_pairs"] == 2


def test_carbon_dioxide_double_bonds():
    s = make("C", "O", "O")
    s.add_bond("0", "1", 2).add_bond("0", "2", 2)
    assert s.is_valid()
    assert classify_vsepr(s)["geometry"] == "lineal"


def test_nitrogen_triple_bond():
    s = make("N", "N")
    s.add_bond("0", "1", 3)
    assert s.is_valid()


def test_carbon_valence_error():
    s = make("C", "H")
    s.add_bond("0", "1", 1)
    assert not s.is_valid()
    assert any(i.code == "valence" for i in s.validate())


def test_disconnected_structure():
    s = make("H", "H", "O")
    s.add_bond("0", "1", 1)
    assert not s.is_valid()
    assert any(i.code == "disconnected" for i in s.validate())
