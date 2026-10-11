from atomos_perdidos.core.molecular_structure import MoleculeStructure
from atomos_perdidos.core.polarity import bond_polarity, molecular_polarity


def make_water():
    s = MoleculeStructure()
    s.add_atom("0", "O").add_atom("1", "H").add_atom("2", "H")
    s.add_bond("0", "1").add_bond("0", "2")
    return s


def make_carbon_dioxide():
    s = MoleculeStructure()
    s.add_atom("0", "C").add_atom("1", "O").add_atom("2", "O")
    s.add_bond("0", "1", 2).add_bond("0", "2", 2)
    return s


def test_oh_bond_is_polar():
    result = bond_polarity("O", "H")
    assert result["supported"]
    assert result["difference"] > 0.4
    assert result["kind"] == "covalente polar"


def test_water_is_polar():
    result = molecular_polarity(make_water())
    assert result["polar"] is True
    assert result["geometry"] == "angular"


def test_carbon_dioxide_is_nonpolar_by_symmetry():
    result = molecular_polarity(make_carbon_dioxide())
    assert result["polar"] is False
    assert result["geometry"] == "lineal"


def test_symmetric_tetrahedral_molecule_is_nonpolar():
    structure = MoleculeStructure()
    for atom_id, symbol in [("c", "C"), ("f1", "F"), ("f2", "F"), ("f3", "F"), ("f4", "F")]:
        structure.add_atom(atom_id, symbol)
    for atom_id in ("f1", "f2", "f3", "f4"):
        structure.add_bond("c", atom_id)
    result = molecular_polarity(structure)
    assert result["supported"]
    assert result["geometry"] == "tetraédrica"
    assert result["polar"] is False


def test_water_is_supported_and_polar_after_vector_sum():
    result = molecular_polarity(make_water())
    assert result["supported"]
    assert result["polar"] is True
    assert result["dipole_magnitude"] > 0.4
