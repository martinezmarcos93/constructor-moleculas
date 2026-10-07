"""Análisis didáctico de polaridad molecular.

Usa electronegatividades de la tabla del proyecto y una aproximación vectorial
basada en la geometría VSEPR conocida. No pretende sustituir cálculos cuánticos.
"""
from __future__ import annotations

import math
from atomos_perdidos.data.periodic_table import ELEMENTS
from atomos_perdidos.core.molecular_structure import MoleculeStructure
from atomos_perdidos.core.vsepr import classify_vsepr


_BY_SYMBOL = {element["symbol"]: element for element in ELEMENTS.values()}


def bond_polarity(symbol_a: str, symbol_b: str) -> dict:
    a = _BY_SYMBOL.get(symbol_a)
    b = _BY_SYMBOL.get(symbol_b)
    if not a or not b:
        raise ValueError("Elemento desconocido.")
    ea, eb = a.get("electronegativity"), b.get("electronegativity")
    if ea is None or eb is None:
        return {"supported": False, "difference": None, "message": "No hay electronegatividad suficiente."}
    diff = round(abs(ea - eb), 3)
    if diff < 0.4:
        kind = "covalente prácticamente no polar"
    elif diff < 1.7:
        kind = "covalente polar"
    else:
        kind = "predominio iónico"
    return {"supported": True, "difference": diff, "kind": kind}


def molecular_polarity(structure: MoleculeStructure) -> dict:
    if not structure.is_valid():
        return {"supported": False, "polar": None, "message": "Corrige la estructura antes de analizar su polaridad."}
    center_id = max(
        structure.atoms,
        key=lambda atom_id: len(structure.neighbors(atom_id))
    )
    center = structure.atoms[center_id]
    neighbors = [structure.atoms[n] for n in structure.neighbors(center_id)]
    if not neighbors:
        return {"supported": False, "polar": None, "message": "No hay enlaces que analizar."}

    vsepr = classify_vsepr(structure)
    differences = [
        bond_polarity(center.symbol, atom.symbol)["difference"]
        for atom in neighbors
        if bond_polarity(center.symbol, atom.symbol)["supported"]
    ]
    if not differences:
        return {"supported": False, "polar": None, "message": "No puedo estimar los dipolos con los datos disponibles."}

    geometry = vsepr.get("geometry")
    symmetric = geometry in {"lineal", "trigonal plana", "tetraédrica", "octaédrica"} and len(set(round(x, 2) for x in differences)) == 1
    polar = bool(max(differences) >= 0.4 and not symmetric)
    if max(differences) < 0.4:
        polar = False
    return {
        "supported": True,
        "polar": polar,
        "center": center.symbol,
        "geometry": geometry,
        "max_bond_difference": max(differences),
        "message": "La geometría permite que los dipolos se cancelen." if not polar else "Los dipolos no se cancelan por completo.",
    }
