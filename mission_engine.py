"""Misiones científicas procedurales para Átomos Perdidos.

El motor transforma la estequiometría en objetivos jugables. No pretende ser
un simulador industrial: las métricas de eficiencia son métricas pedagógicas
explícitas para comparar estrategias del jugador.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import math
import re

from reaction_engine import reaction_quantities


@dataclass(frozen=True)
class MissionSpec:
    id: str
    title: str
    briefing: str
    reactants: tuple[str, ...]
    products: tuple[str, ...]
    target_product: str
    target_moles: float
    max_total_input: float
    max_waste_fraction: float
    min_utilization: float
    difficulty: int
    concepts: tuple[str, ...]
    reward_xp: int
    reward_credits: int

    def serialize(self) -> dict:
        return asdict(self)


MISSION_TEMPLATES = (
    {
        "id": "fabrica_agua",
        "title": "La fábrica de agua",
        "briefing": "Produce la cantidad solicitada de agua sin malgastar recursos.",
        "reactants": ("H2", "O2"), "products": ("H2O",),
        "concepts": ("balanceo", "reactivo_limitante", "estequiometria"),
    },
    {
        "id": "planta_amoniaco",
        "title": "La planta de amoníaco",
        "briefing": "Obtén amoníaco a partir de nitrógeno e hidrógeno respetando la proporción de reacción.",
        "reactants": ("N2", "H2"), "products": ("NH3",),
        "concepts": ("balanceo", "reactivo_limitante", "estequiometria", "proporcion"),
    },
)


def _seed_value(seed: str | int | None, difficulty: int) -> int:
    raw = f"{seed or 'default'}:{difficulty}".encode("utf-8")
    return int(hashlib.sha256(raw).hexdigest()[:12], 16)


def generate_mission(mission_id: str | None = None, difficulty: int = 1, seed: str | int | None = None) -> dict:
    difficulty = max(1, min(5, int(difficulty)))
    index = _seed_value(seed, difficulty) % len(MISSION_TEMPLATES)
    if mission_id:
        for i, template in enumerate(MISSION_TEMPLATES):
            if template["id"] == mission_id:
                index = i
                break
        else:
            raise ValueError("Misión desconocida.")
    template = MISSION_TEMPLATES[index]

    exact = re.search(r"-d(\\d+)-(\\d+)$", str(mission_id or ""))
    if exact:
        difficulty = max(1, min(5, int(exact.group(1))))
        multiplier = int(exact.group(2))
    else:
        multiplier = 1 + ((_seed_value(seed, difficulty) // 7) % (2 + difficulty))
    target = float(multiplier)
    # A mayor dificultad, se estrecha la tolerancia de desperdicio y el margen.
    tolerance = max(0.05, 0.25 - difficulty * 0.03)
    min_utilization = min(0.98, 0.72 + difficulty * 0.05)
    # El presupuesto parte de la proporción estequiométrica ideal y agrega margen.
    if template["id"] == "fabrica_agua":
        ideal_input = target * 3.0
    else:
        # N2 + 3 H2 -> 2 NH3
        ideal_input = target * 2.0
    budget = round(ideal_input * (1.0 + tolerance), 2)

    spec = MissionSpec(
        id=f"{template['id']}-d{difficulty}-{multiplier}",
        title=template["title"],
        briefing=template["briefing"],
        reactants=template["reactants"],
        products=template["products"],
        target_product=template["products"][0],
        target_moles=target,
        max_total_input=budget,
        max_waste_fraction=round(tolerance, 3),
        min_utilization=round(min_utilization, 3),
        difficulty=difficulty,
        concepts=template["concepts"],
        reward_xp=10 + difficulty * 5,
        reward_credits=2 + difficulty,
    )
    return spec.serialize()


def list_missions() -> list[dict]:
    return [generate_mission(t["id"], d, seed=f"{t['id']}:catalog") for d in range(1, 4) for t in MISSION_TEMPLATES]


def _reaction_result(spec: dict, amounts: dict) -> dict:
    quantities = []
    for reagent in spec["reactants"]:
        try:
            value = float(amounts.get(reagent, 0))
        except (TypeError, ValueError):
            raise ValueError(f"La cantidad de {reagent} no es válida.")
        if value <= 0:
            raise ValueError(f"La cantidad de {reagent} debe ser mayor que cero.")
        quantities.append(value)
    return reaction_quantities(spec["reactants"], spec["products"], quantities)


def evaluate_mission(spec: dict, amounts: dict, prediction: str | None = None) -> dict:
    result = _reaction_result(spec, amounts)
    target_name = spec["target_product"]
    theoretical = next(
        (p["theoretical_moles"] for p in result["products"] if p["formula"] == target_name), 0.0
    )
    total_input = sum(float(amounts[r]) for r in spec["reactants"])
    remaining = sum(max(0.0, float(r["remaining_moles"])) for r in result["reactants"])
    utilization = 0.0 if total_input <= 0 else max(0.0, min(1.0, 1.0 - remaining / total_input))
    waste_fraction = 1.0 - utilization
    target_met = theoretical + 1e-9 >= float(spec["target_moles"])
    within_budget = total_input <= float(spec["max_total_input"]) + 1e-9
    waste_ok = waste_fraction <= float(spec["max_waste_fraction"]) + 1e-9
    utilization_ok = utilization + 1e-9 >= float(spec["min_utilization"])

    limiting = result.get("limiting_reagent")
    prediction_ok = prediction is None or prediction == limiting

    score = 0
    score += 35 if target_met else round(35 * min(1, theoretical / max(float(spec["target_moles"]), 1e-9)))
    score += 20 if within_budget else 0
    score += 20 if waste_ok else round(max(0, 20 * (1 - waste_fraction / max(float(spec["max_waste_fraction"]) * 2, 0.01))))
    score += 20 if utilization_ok else round(20 * utilization / max(float(spec["min_utilization"]), 0.01))
    score += 5 if prediction_ok else 0
    score = max(0, min(100, int(score)))

    completed = target_met and within_budget and waste_ok and utilization_ok
    perfect = completed and prediction_ok and score >= 90
    status = "perfect" if perfect else "completed" if completed else "failed"

    reward_scale = 1.0 if perfect else 0.75 if completed else 0.0
    reward = {
        "xp": round(float(spec["reward_xp"]) * reward_scale),
        "credits": round(float(spec["reward_credits"]) * reward_scale),
        "rank": "maestro" if perfect else "experto" if completed else "sin_éxito",
    }

    return {
        "status": status,
        "completed": completed,
        "perfect": perfect,
        "score": score,
        "target": {"product": target_name, "moles": float(spec["target_moles"])},
        "theoretical_product_moles": theoretical,
        "limiting_reagent": limiting,
        "total_input_moles": round(total_input, 6),
        "remaining_moles": round(remaining, 6),
        "utilization": round(utilization, 6),
        "waste_fraction": round(waste_fraction, 6),
        "constraints": {
            "target_met": target_met,
            "within_budget": within_budget,
            "waste_ok": waste_ok,
            "utilization_ok": utilization_ok,
        },
        "prediction": {"value": prediction, "correct": prediction_ok},
        "reaction": result,
        "reward": reward,
    }


def mission_hint(spec: dict) -> str:
    if spec["reactants"] == ("H2", "O2"):
        return "La ecuación exige 2 mol de H₂ por cada 1 mol de O₂."
    if spec["reactants"] == ("N2", "H2"):
        return "La ecuación exige 1 mol de N₂ por cada 3 mol de H₂."
    return "Primero balancea la reacción y después calcula la proporción de reactivos."
