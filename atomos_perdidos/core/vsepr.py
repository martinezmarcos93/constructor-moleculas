"""Clasificación VSEPR introductoria para estructuras sencillas."""
from __future__ import annotations

from atomos_perdidos.core.molecular_structure import MoleculeStructure

VSEPR_SHAPES = {
    (2, 0): ("lineal", "AX₂", 180),
    (3, 0): ("trigonal plana", "AX₃", 120),
    (3, 1): ("angular", "AX₂E", 120),
    (4, 0): ("tetraédrica", "AX₄", 109.5),
    (4, 1): ("piramidal trigonal", "AX₃E", 107),
    (4, 2): ("angular", "AX₂E₂", 104.5),
    (5, 0): ("bipiramidal trigonal", "AX₅", 90),
    (6, 0): ("octaédrica", "AX₆", 90),
}

_VALENCE_ELECTRONS = {
    "H": 1, "B": 3, "C": 4, "N": 5, "O": 6, "F": 7,
    "P": 5, "S": 6, "Cl": 7, "Br": 7, "I": 7,
}


def _central_atom(structure: MoleculeStructure) -> str | None:
    if not structure.atoms:
        return None
    ranked = sorted(
        structure.atoms.values(),
        key=lambda a: (
            len(structure.neighbors(a.id)),
            a.symbol != "H",
            a.symbol in {"C", "N", "O", "S", "P"},
        ),
        reverse=True,
    )
    return ranked[0].id


def classify_vsepr(structure: MoleculeStructure) -> dict:
    center_id = _central_atom(structure)
    if center_id is None:
        return {"supported": False, "message": "No hay átomo central."}

    center = structure.atoms[center_id]
    neighbors = structure.neighbors(center_id)
    if not neighbors:
        return {"supported": False, "message": "El átomo central no tiene vecinos."}
    if any(b.kind != "covalent" for b in structure.bonds if center_id in (b.a, b.b)):
        return {"supported": False, "message": "VSEPR no se aplica a enlaces iónicos en este modo."}

    total = _VALENCE_ELECTRONS.get(center.symbol)
    if total is None:
        return {"supported": False, "message": f"VSEPR aún no cubre {center.symbol}."}

    # Este modelo neutral simplificado cuenta los electrones no enlazantes que
    # quedan en el átomo central; cada enlace covalente consume un electrón suyo.
    bond_order_sum = structure.bond_order_sum(center_id)
    lone_pairs = max(0, (total - bond_order_sum) // 2)
    if center.symbol == "C" and bond_order_sum == 4:
        lone_pairs = 0
    elif center.symbol == "N" and bond_order_sum == 3:
        lone_pairs = 1
    elif center.symbol == "O" and bond_order_sum == 2:
        lone_pairs = 2
    elif center.symbol == "S" and bond_order_sum == 6:
        lone_pairs = 0

    # La primera coordenada representa dominios electrónicos totales: enlaces + pares solitarios.
    # Ej.: H2O = 2 enlaces + 2 pares solitarios -> (4, 2); NH3 -> (4, 1).
    domains = len(neighbors) + lone_pairs
    shape = VSEPR_SHAPES.get((domains, lone_pairs))
    if not shape:
        return {
            "supported": False,
            "center": center.symbol,
            "domains": domains,
            "lone_pairs": lone_pairs,
            "message": "La geometría está fuera del conjunto introductorio.",
        }
    name, notation, angle = shape
    return {
        "supported": True,
        "center": center.symbol,
        "domains": domains,
        "lone_pairs": lone_pairs,
        "geometry": name,
        "notation": notation,
        "ideal_angle": angle,
    }
