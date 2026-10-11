import pytest

from atomos_perdidos.core.molecular_structure import MoleculeStructure


def test_rejects_unknown_element_symbol():
    structure = MoleculeStructure()
    with pytest.raises(ValueError, match="Símbolo químico desconocido"):
        structure.add_atom("x", "Xx")


def test_rejects_self_bond():
    structure = MoleculeStructure().add_atom("1", "H")
    with pytest.raises(ValueError, match="consigo mismo"):
        structure.add_bond("1", "1")


def test_rejects_duplicate_bond_even_with_reversed_endpoints():
    structure = MoleculeStructure().add_atom("1", "H").add_atom("2", "H")
    structure.add_bond("1", "2")
    with pytest.raises(ValueError, match="Ya existe un enlace"):
        structure.add_bond("2", "1")
