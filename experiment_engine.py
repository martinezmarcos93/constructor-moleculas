"""Motor jugable de experimentos educativos.

El motor separa cuatro momentos: predicción, ejecución, observación y conclusión.
Los resultados se calculan con los motores químicos existentes siempre que sea
posible; no se pretende simular química experimental profesional.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from copy import deepcopy

from molecular_structure import MoleculeStructure
from polarity import molecular_polarity
from reaction_engine import balance_equation
from stoichiometry import analyze_formula_stoichiometry


@dataclass(frozen=True)
class ExperimentSpec:
    id: str
    title: str
    hypothesis_prompt: str
    variables: tuple[str, ...]
    steps: tuple[str, ...]
    concept: str
    prediction_options: tuple[str, ...]
    expected_prediction: str


@dataclass
class ExperimentRun:
    spec: ExperimentSpec
    prediction: str | None = None
    observations: list[str] = field(default_factory=list)
    result: dict | None = None
    score: int = 0
    completed: bool = False

    def predict(self, value: str) -> dict:
        if value not in self.spec.prediction_options:
            raise ValueError("Predicción no válida para este experimento.")
        self.prediction = value
        return {"prediction": value, "correct": value == self.spec.expected_prediction}

    def observe(self, observation: str) -> None:
        observation = observation.strip()
        if observation:
            self.observations.append(observation)

    def evaluate(self, result: dict) -> dict:
        self.result = deepcopy(result)
        prediction_ok = self.prediction == self.spec.expected_prediction
        observation_ok = bool(self.observations)
        self.score = (60 if prediction_ok else 20) + (40 if observation_ok else 0)
        self.completed = True
        return self.report()

    def report(self) -> dict:
        return {
            "id": self.spec.id,
            "title": self.spec.title,
            "concept": self.spec.concept,
            "hypothesis_prompt": self.spec.hypothesis_prompt,
            "variables": list(self.spec.variables),
            "steps": list(self.spec.steps),
            "prediction_options": list(self.spec.prediction_options),
            "prediction": self.prediction,
            "observations": list(self.observations),
            "result": self.result,
            "score": self.score,
            "completed": self.completed,
        }


EXPERIMENT_SPECS = (
    ExperimentSpec(
        "polaridad_agua",
        "El misterio de H₂O",
        "Predice si la geometría de H₂O permite cancelar sus dipolos.",
        ("estructura", "geometría", "electronegatividad"),
        ("Construye H₂O.", "Valida la estructura.", "Analiza la polaridad.", "Explica el resultado."),
        "polaridad",
        ("polar", "no_polar"),
        "polar",
    ),
    ExperimentSpec(
        "conservacion_materia",
        "El átomo no desaparece",
        "Predice si el número de átomos de cada elemento puede cambiar durante una reacción.",
        ("reactivos", "productos", "coeficientes"),
        ("Elige una reacción.", "Balancea los coeficientes.", "Compara los átomos.", "Formula una conclusión."),
        "conservacion",
        ("se_conserva", "no_se_conserva"),
        "se_conserva",
    ),
    ExperimentSpec(
        "masa_molar",
        "¿Cuánto pesa una molécula?",
        "Predice cuál de dos fórmulas tiene mayor masa molar.",
        ("fórmula", "masa_atómica", "proporción"),
        ("Compara las fórmulas.", "Calcula sus masas molares.", "Comprueba tu predicción."),
        "estequiometria",
        ("primera_mayor", "segunda_mayor"),
        "primera_mayor",
    ),
)


def _structure_from_payload(data: dict) -> MoleculeStructure:
    structure = MoleculeStructure()
    for atom in data.get("atoms", [])[:60]:
        structure.add_atom(str(atom["id"]), atom["symbol"])
    for bond in data.get("bonds", [])[:120]:
        structure.add_bond(
            str(bond["a"]),
            str(bond["b"]),
            int(bond.get("order", 1)),
            str(bond.get("kind", "covalent")),
        )
    return structure


def run_experiment(experiment_id: str, payload: dict) -> dict:
    spec = next((item for item in EXPERIMENT_SPECS if item.id == experiment_id), None)
    if not spec:
        raise ValueError("Experimento no encontrado.")

    prediction = payload.get("prediction")
    observations = payload.get("observations", [])
    run = ExperimentRun(spec, prediction=prediction)
    for observation in observations if isinstance(observations, list) else []:
        run.observe(str(observation))

    if experiment_id == "polaridad_agua":
        structure = _structure_from_payload(payload)
        result = molecular_polarity(structure)
        if not result.get("supported"):
            raise ValueError(result.get("message", "No se pudo analizar la estructura."))
        return run.evaluate(result)

    if experiment_id == "conservacion_materia":
        equation = payload.get("equation", {})
        result = balance_equation(
            equation.get("reactants", []),
            equation.get("products", []),
        )
        if not result.get("conserved"):
            raise ValueError("La ecuación no pudo conservar los elementos.")
        return run.evaluate(result)

    if experiment_id == "masa_molar":
        formulas = payload.get("formulas", [])
        if len(formulas) != 2:
            raise ValueError("Se necesitan exactamente dos fórmulas.")
        first = analyze_formula_stoichiometry(formulas[0])
        second = analyze_formula_stoichiometry(formulas[1])
        if not first.get("ok") or not second.get("ok"):
            raise ValueError("No pude analizar ambas fórmulas.")
        result = {
            "first": first,
            "second": second,
            "greater": "first" if first["molar_mass"] > second["molar_mass"] else "second",
        }
        return run.evaluate(result)

    raise ValueError("Experimento sin ejecución implementada.")


def get_experiment(experiment_id: str) -> ExperimentSpec | None:
    return next((item for item in EXPERIMENT_SPECS if item.id == experiment_id), None)


def list_experiments() -> list[dict]:
    return [
        {
            "id": item.id,
            "title": item.title,
            "concept": item.concept,
            "hypothesis_prompt": item.hypothesis_prompt,
            "variables": list(item.variables),
            "steps": list(item.steps),
            "prediction_options": list(item.prediction_options),
        }
        for item in EXPERIMENT_SPECS
    ]
