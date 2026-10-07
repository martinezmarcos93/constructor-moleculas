"""Metadatos pedagógicos para desafíos de Átomos Perdidos.

Permite que una misma molécula se convierta en ejercicios de dificultad
creciente sin duplicar el contenido químico.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Challenge:
    id: str
    molecule_id: str
    mode: str
    difficulty: int
    concepts: tuple[str, ...]
    prompt: str


def concepts_for(molecule: dict) -> tuple[str, ...]:
    atoms = set(molecule.get("atoms", []))
    concepts = ["atoms", "periodic_table"]
    if len(atoms) >= 2:
        concepts.append("chemical_bonds")
    if "C" in atoms or "Si" in atoms:
        concepts.append("covalent_bonds")
    if any(s in atoms for s in ("Na", "K", "Li", "Mg", "Ca")):
        concepts.append("ionic_bonds")
    if len(molecule.get("atoms", [])) >= 3:
        concepts.append("molecular_structure")
    if molecule.get("svg_key") in {"H2O", "NH3", "CH4", "CO2", "SO2", "SF6", "PCl3"}:
        concepts.append("vsepr")
    if "C" in atoms and len(atoms) >= 4:
        concepts.append("organic_chemistry")
    return tuple(dict.fromkeys(concepts))


def build_challenges(molecules: dict[str, list[dict]]) -> list[Challenge]:
    challenges = []
    for level, entries in molecules.items():
        if level == "story":
            continue
        for molecule in entries:
            concepts = concepts_for(molecule)
            base = {"easy": 1, "medium": 2, "hard": 3}.get(level, 1)
            challenges.extend([
                Challenge(
                    id=f"{molecule['id']}:complete",
                    molecule_id=molecule["id"],
                    mode="complete",
                    difficulty=base,
                    concepts=concepts,
                    prompt=f"Completa {molecule['name']} usando la tabla periódica.",
                ),
                Challenge(
                    id=f"{molecule['id']}:identify",
                    molecule_id=molecule["id"],
                    mode="identify",
                    difficulty=min(5, base + 1),
                    concepts=concepts + ("formula",),
                    prompt=f"Identifica la fórmula correcta de {molecule['name']}.",
                ),
            ])
    return challenges


def serialize_challenges(molecules: dict[str, list[dict]]) -> list[dict]:
    return [asdict(c) for c in build_challenges(molecules)]
