"""Clasificación VSEPR introductoria para estructuras sencillas."""
from __future__ import annotations

from molecular_structure import MoleculeStructure

# Conteo de dominios electrónicos para los casos cubiertos por el juego.
# Se prioriza una regla estable y explicable antes que una cobertura total.
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


def _central_atom(structure: MoleculeStructure) -> str | None:
    if not structure.atoms:
        return None
    # En estructuras pequeñas, el átomo con mayor conectividad es un centro
    # razonable para el modo didáctico. En empate se prefiere el no-H.
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

    # Para el nivel introductorio contamos enlaces múltiples como un dominio
    # electrónico, no como varios dominios.
    domains = len(neighbors)

    # Electrones de valencia del átomo central y de sus vecinos.
    # La heurística de pares solitarios funciona para los elementos del bloque
    # principal cubiertos por las moléculas del juego.
    valence = {
        "H": 1, "B": 3, "C": 4, "N": 5, "O": 6,
        "F": 7, "P": 5, "S": 6, "Cl": 7,
    }
    total = valence.get(center.symbol)
    if total is None:
        return {"supported": False, "message": f"VSEPR aún no cubre {center.symbol}."}

    bond_order_sum = structure.bond_order_sum(center_id)
    nonbonding_electrons = max(0, total - bond_order_sum * 1)
    lone_pairs = nonbonding_electrons // 2
    # Ajuste didáctico: los enlaces covalentes consumen un electrón del átomo
    # central por orden de enlace; para moléculas neutras sencillas esto permite
    # reconocer H2O, NH3, CH4, CO2, SO2 y SF6.
    if center.symbol == "N" and bond_order_sum == 3:
        lone_pairs = 1
    elif center.symbol == "O" and bond_order_sum == 2:
        lone_pairs = 2
    elif center.symbol == "C" and bond_order_sum == 4:
        lone_pairs = 0
    elif center.symbol == "S" and bond_order_sum in (4, 6):
        lone_pairs = 0 if bond_order_sum == 6 else 1
    key = (domains, lone_pairs)
    shape = VSEPR_SHAPES.get(key)
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
