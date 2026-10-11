"""Análisis didáctico de polaridad molecular por cancelación aproximada de dipolos."""
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


def _vector_norm(vector: tuple[float, float, float]) -> float:
    return math.sqrt(sum(component * component for component in vector))


def molecular_polarity(structure: MoleculeStructure) -> dict:
    if not structure.is_valid():
        return {"supported": False, "polar": None, "message": "Corrige la estructura antes de analizar su polaridad."}
    if any(b.kind != "covalent" for b in structure.bonds):
        return {"supported": False, "polar": None, "message": "El análisis de polaridad sólo cubre estructuras covalentes en este modo."}

    center_id = max(
        structure.atoms,
        key=lambda atom_id: (
            len(structure.neighbors(atom_id)),
            structure.atoms[atom_id].symbol != "H",
        ),
    )
    center = structure.atoms[center_id]
    neighbor_ids = structure.neighbors(center_id)
    if not neighbor_ids:
        return {"supported": False, "polar": None, "message": "No hay enlaces que analizar."}

    vsepr = classify_vsepr(structure)
    if not vsepr.get("supported"):
        return {"supported": False, "polar": None, "message": vsepr.get("message", "Geometría no soportada.")}

    # Geometría ideal para los casos del currículo que tiene una disposición
    # inequívoca. El módulo no pretende inferir coordenadas de cualquier isómero.
    geometry_vectors = {
        "lineal": [(1.0, 0.0, 0.0), (-1.0, 0.0, 0.0)],
        "angular": None,
        "trigonal plana": [(1.0, 0.0, 0.0), (-0.5, math.sqrt(3) / 2, 0.0),
                           (-0.5, -math.sqrt(3) / 2, 0.0)],
        "tetraédrica": [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)],
        "piramidal trigonal": [(1, 0, 0.6), (-0.5, math.sqrt(3) / 2, 0.6),
                               (-0.5, -math.sqrt(3) / 2, 0.6)],
        "octaédrica": [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)],
    }
    geometry = vsepr.get("geometry")
    if geometry == "angular" and len(neighbor_ids) == 2:
        # Ángulo de 104,5° para H2O; dirección del dipolo resultante, no su módulo absoluto.
        half = math.radians(104.5 / 2)
        vectors = [(math.sin(half), math.cos(half), 0.0),
                   (-math.sin(half), math.cos(half), 0.0)]
    else:
        vectors = geometry_vectors.get(geometry)
    if vectors is None or len(vectors) != len(neighbor_ids):
        return {"supported": False, "polar": None, "geometry": geometry,
                "message": "Esta disposición molecular no está incluida en el modelo vectorial didáctico."}

    dipole = [0.0, 0.0, 0.0]
    differences = []
    for neighbor_id, vector in zip(neighbor_ids, vectors):
        neighbor = structure.atoms[neighbor_id]
        bond = bond_polarity(center.symbol, neighbor.symbol)
        if not bond["supported"]:
            return {"supported": False, "polar": None,
                    "message": "No hay electronegatividades suficientes para estimar todos los enlaces."}
        diff = bond["difference"]
        differences.append(diff)
        norm = _vector_norm(vector)
        for index in range(3):
            dipole[index] += (vector[index] / norm) * diff

    magnitude = _vector_norm(tuple(dipole))
    # El umbral evita confundir residuos numéricos de simetrías ideales con polaridad.
    polar = magnitude >= 0.4
    return {
        "supported": True,
        "polar": polar,
        "center": center.symbol,
        "geometry": geometry,
        "max_bond_difference": max(differences),
        "dipole_magnitude": round(magnitude, 4),
        "message": "Los dipolos se cancelan aproximadamente." if not polar else "Los dipolos no se cancelan por completo.",
    }
