from atomos_perdidos.core.reaction_engine import balance_equation
from atomos_perdidos.data.reactions import REACTIONS


def test_catalog_reactions_are_atom_conserving():
    for reaction in REACTIONS:
        data = reaction["balance"]
        result = balance_equation(data["reactants"], data["products"])
        assert result["conserved"] is True
