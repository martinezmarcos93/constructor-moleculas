from atomos_perdidos.core.molecular_structure import MoleculeStructure
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


def test_methane_has_tetrahedral_geometry():
    s = make("C", "H", "H", "H", "H")
    for i in range(1, 5):
        s.add_bond("0", str(i), 1)
    assert s.is_valid()
    result = classify_vsepr(s)
    assert result["geometry"] == "tetraédrica"
    assert result["lone_pairs"] == 0


def test_ammonia_is_trigonal_pyramidal():
    s = make("N", "H", "H", "H")
    for i in range(1, 4):
        s.add_bond("0", str(i), 1)
    result = classify_vsepr(s)
    assert s.is_valid()
    assert result["geometry"] == "piramidal trigonal"


def test_ionic_bond_does_not_consume_covalent_valence():
    s = make("Na", "Cl")
    s.add_bond("0", "1", 1, kind="ionic")
    assert s.is_valid()
    assert s.formula() == "NaCl"
