from __future__ import annotations
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
    answer: str | None = None


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
            geometry = {
                "H2O": ("angular", "¿Qué geometría molecular presenta el agua?"),
                "CO2": ("lineal", "¿Qué geometría molecular presenta el CO₂?"),
                "NH3": ("piramidal trigonal", "¿Qué geometría molecular presenta el NH₃?"),
                "CH4": ("tetraédrica", "¿Qué geometría molecular presenta el CH₄?"),
                "SO2": ("angular", "¿Qué geometría molecular presenta el SO₂?"),
                "SF6": ("octaédrica", "¿Qué geometría molecular presenta el SF₆?"),
                "PCl3": ("piramidal trigonal", "¿Qué geometría molecular presenta el PCl₃?"),
            }.get(molecule.get("svg_key"))
            if geometry:
                answer, prompt = geometry
                challenges.append(Challenge(
                    id=f"{molecule['id']}:geometry",
                    molecule_id=molecule["id"],
                    mode="geometry",
                    difficulty=min(5, base + 2),
                    concepts=concepts + ("molecular_geometry",),
                    prompt=prompt,
                    answer=answer,
                ))
    return challenges


def serialize_challenges(molecules: dict[str, list[dict]]) -> list[dict]:
    return [asdict(c) for c in build_challenges(molecules)]


def generate_procedural_challenge(molecules: dict[str, list[dict]], difficulty: int = 1, seed: int | None = None) -> dict:
    """Genera un desafío reproducible a partir del catálogo actual."""
    import hashlib
    import random

    entries = [m for level, values in molecules.items() if level != "story" for m in values]
    if not entries:
        raise ValueError("No hay moléculas disponibles.")
    difficulty = max(1, min(5, int(difficulty)))
    digest = hashlib.sha256(f"{seed}:{difficulty}".encode()).hexdigest()
    rng = random.Random(int(digest[:12], 16))
    molecule = rng.choice(entries)
    concepts = concepts_for(molecule)
    modes = ["identify", "formula", "atoms"]
    if molecule.get("svg_key") in {"H2O", "NH3", "CH4", "CO2", "SO2", "SF6", "PCl3"}:
        modes.append("geometry")
    mode = modes[(difficulty + rng.randrange(len(modes))) % len(modes)]
    if mode == "formula":
        prompt = f"Escribe la fórmula de {molecule['name']}."
        answer = molecule.get("formula")
    elif mode == "atoms":
        prompt = f"¿Cuántos átomos contiene en total {molecule['name']}?"
        answer = str(len(molecule.get("atoms", [])))
    elif mode == "geometry":
        answer, prompt = {
            "H2O": ("angular", "¿Qué geometría molecular presenta el H₂O?"),
            "CO2": ("lineal", "¿Qué geometría molecular presenta el CO₂?"),
            "NH3": ("piramidal trigonal", "¿Qué geometría molecular presenta el NH₃?"),
            "CH4": ("tetraédrica", "¿Qué geometría molecular presenta el CH₄?"),
            "SO2": ("angular", "¿Qué geometría molecular presenta el SO₂?"),
            "SF6": ("octaédrica", "¿Qué geometría molecular presenta el SF₆?"),
            "PCl3": ("piramidal trigonal", "¿Qué geometría molecular presenta el PCl₃?"),
        }.get(molecule.get("svg_key"), ("", "Analiza la geometría de la molécula."))
    else:
        prompt = f"Identifica la fórmula correcta de {molecule['name']}."
        answer = molecule.get("formula")
    return {
        "id": f"procedural:{molecule['id']}:{mode}:{digest[:8]}",
        "molecule_id": molecule["id"],
        "mode": mode,
        "difficulty": difficulty,
        "concepts": concepts + (("procedural",) if "procedural" not in concepts else ()),
        "prompt": prompt,
        "answer": answer,
    }


def evaluate_challenge(challenge: dict, answer) -> dict:
    """Evalúa una respuesta generada, con normalización textual básica."""
    expected = challenge.get("answer")
    if expected is None:
        raise ValueError("El desafío no tiene una respuesta evaluable.")
    given = str(answer).strip().casefold()
    target = str(expected).strip().casefold()
    correct = given == target
    score = 100 if correct else 0
    if not correct and challenge.get("mode") == "atoms":
        try:
            correct = int(float(answer)) == int(expected)
            score = 100 if correct else 0
        except (TypeError, ValueError):
            pass
    return {
        "correct": correct,
        "score": score,
        "answer": expected,
        "feedback": "Correcto. El concepto queda reforzado." if correct else "Todavía no. Revisa la pista conceptual y vuelve a intentarlo.",
    }
