"""Motor de laboratorio experimental para Átomos Perdidos.

Las variables son deliberadamente educativas: el motor calcula relaciones
químicas conocidas sin fingir una simulación profesional de laboratorio.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from copy import deepcopy

from molecular_structure import MoleculeStructure
from polarity import molecular_polarity
from reaction_engine import balance_equation, reaction_quantities
from stoichiometry import analyze_formula_stoichiometry


@dataclass(frozen=True)
class VariableSpec:
    id: str
    label: str
    kind: str
    minimum: float | None = None
    maximum: float | None = None
    step: float | None = None
    options: tuple[str, ...] = ()

    def serialize(self) -> dict:
        return {
            "id": self.id, "label": self.label, "kind": self.kind,
            "minimum": self.minimum, "maximum": self.maximum,
            "step": self.step, "options": list(self.options),
        }


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
    controls: tuple[VariableSpec, ...]


@dataclass
class ExperimentRun:
    spec: ExperimentSpec
    prediction: str | None = None
    observations: list[str] = field(default_factory=list)
    variables: dict = field(default_factory=dict)
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

    def set_variables(self, values: dict) -> None:
        for control in self.spec.controls:
            if control.id not in values:
                continue
            value = values[control.id]
            if control.kind == "choice":
                if value not in control.options:
                    raise ValueError(f"Valor no permitido para {control.label}.")
                self.variables[control.id] = value
            else:
                try:
                    numeric = float(value)
                except (TypeError, ValueError):
                    raise ValueError(f"{control.label} debe ser numérico.")
                if control.minimum is not None and numeric < control.minimum:
                    raise ValueError(f"{control.label} está por debajo del mínimo.")
                if control.maximum is not None and numeric > control.maximum:
                    raise ValueError(f"{control.label} está por encima del máximo.")
                self.variables[control.id] = numeric

    def evaluate(self, result: dict) -> dict:
        self.result = deepcopy(result)
        prediction_ok = self.prediction == self.spec.expected_prediction
        observation_ok = bool(self.observations)
        variable_ok = bool(self.variables)
        self.score = (50 if prediction_ok else 15) + (30 if observation_ok else 0) + (20 if variable_ok else 0)
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
            "controls": [c.serialize() for c in self.spec.controls],
            "prediction": self.prediction,
            "observations": list(self.observations),
            "variables_used": dict(self.variables),
            "result": self.result,
            "score": self.score,
            "completed": self.completed,
        }


EXPERIMENT_SPECS = (
    ExperimentSpec(
        "polaridad_agua", "El misterio de H₂O",
        "Predice si cambiar la geometría o el entorno altera la polaridad observable.",
        ("estructura", "geometría", "electronegatividad"),
        ("Construye H₂O.", "Elige condiciones de observación.", "Predice.", "Ejecuta y compara."),
        "polaridad", ("polar", "no_polar"), "polar",
        (VariableSpec("temperature", "Temperatura de observación (°C)", "number", -20, 100, 10),),
    ),
    ExperimentSpec(
        "conservacion_materia", "El átomo no desaparece",
        "Predice qué ocurre con los átomos cuando cambias la cantidad de reactivo.",
        ("reactivos", "productos", "coeficientes"),
        ("Elige reactivos.", "Modifica la cantidad inicial.", "Balancea.", "Compara evidencia."),
        "conservacion", ("se_conserva", "no_se_conserva"), "se_conserva",
        (VariableSpec("reactant_amount", "Cantidad de H₂ (unidades)", "number", 1, 10, 1),
         VariableSpec("oxygen_amount", "Cantidad de O₂ (unidades)", "number", 1, 10, 1)),
    ),
    ExperimentSpec(
        "rendimiento_reaccion", "La fábrica molecular",
        "Predice qué reactivo se agotará primero y cuánto producto podrá formarse.",
        ("reactivos", "estequiometría", "reactivo limitante", "rendimiento"),
        ("Selecciona la reacción.", "Asigna cantidades iniciales.", "Predice el reactivo limitante.", "Ejecuta.", "Analiza el exceso."),
        "reacciones", ("reactivo_1", "reactivo_2"), "reactivo_1",
        (VariableSpec("first_moles", "Cantidad del primer reactivo (mol)", "number", 0.1, 20, 0.1),
         VariableSpec("second_moles", "Cantidad del segundo reactivo (mol)", "number", 0.1, 20, 0.1)),
    ),
    ExperimentSpec(
        "masa_molar", "¿Cuánto pesa una molécula?",
        "Predice cuál muestra tendrá mayor masa total al cambiar la cantidad.",
        ("fórmula", "masa_atómica", "proporción"),
        ("Selecciona las muestras.", "Modifica sus cantidades.", "Calcula.", "Compara evidencia."),
        "estequiometria", ("primera_mayor", "segunda_mayor"), "segunda_mayor",
        (VariableSpec("first_amount", "Cantidad de H₂O", "number", 1, 20, 1),
         VariableSpec("second_amount", "Cantidad de CO₂", "number", 1, 20, 1)),
    ),
)


def _structure_from_payload(data: dict) -> MoleculeStructure:
    structure = MoleculeStructure()
    for atom in data.get("atoms", [])[:60]:
        structure.add_atom(str(atom["id"]), atom["symbol"])
    for bond in data.get("bonds", [])[:120]:
        structure.add_bond(str(bond["a"]), str(bond["b"]), int(bond.get("order", 1)), str(bond.get("kind", "covalent")))
    return structure


def run_experiment(experiment_id: str, payload: dict) -> dict:
    spec = next((item for item in EXPERIMENT_SPECS if item.id == experiment_id), None)
    if not spec:
        raise ValueError("Experimento no encontrado.")
    run = ExperimentRun(spec, prediction=payload.get("prediction"))
    run.set_variables(payload.get("variables", {}))
    observations = payload.get("observations", [])
    for observation in observations if isinstance(observations, list) else []:
        run.observe(str(observation))

    if experiment_id == "polaridad_agua":
        result = molecular_polarity(_structure_from_payload(payload))
        if not result.get("supported"):
            raise ValueError(result.get("message", "No se pudo analizar la estructura."))
        result["controlled_temperature_c"] = run.variables.get("temperature")
        result["interpretation"] = "La temperatura se registra como variable experimental; la polaridad estructural calculada no se modifica artificialmente por ella."
        return run.evaluate(result)

    if experiment_id == "conservacion_materia":
        h2 = int(run.variables.get("reactant_amount", 1))
        o2 = int(run.variables.get("oxygen_amount", 1))
        result = balance_equation(["H2", "O2"], ["H2O"])
        result["initial_amounts"] = {"H2": h2, "O2": o2}
        result["limiting_reagent"] = "H2" if h2 / 2 < o2 else "O2" if o2 < h2 / 2 else "ninguno"
        result["interpretation"] = "Cambiar cantidades modifica cuánto producto puede formarse, pero no elimina la conservación de átomos."
        return run.evaluate(result)

    if experiment_id == "rendimiento_reaccion":
        first = run.variables.get("first_moles", 1.0)
        second = run.variables.get("second_moles", 1.0)
        result = reaction_quantities(["H2", "O2"], ["H2O"], [first, second])
        result["interpretation"] = (
            "El reactivo limitante fija el máximo teórico de producto; "
            "el reactivo restante queda en exceso."
        )
        return run.evaluate(result)

    if experiment_id == "masa_molar":
        first = analyze_formula_stoichiometry("H₂O")
        second = analyze_formula_stoichiometry("CO₂")
        a = run.variables.get("first_amount", 1)
        b = run.variables.get("second_amount", 1)
        first_total = first["molar_mass"] * a
        second_total = second["molar_mass"] * b
        result = {
            "first": first, "second": second,
            "amounts": {"H₂O": a, "CO₂": b},
            "total_masses": {"H₂O": first_total, "CO₂": second_total},
            "greater": "first" if first_total > second_total else "second" if second_total > first_total else "equal",
        }
        result["interpretation"] = "La masa total depende tanto de la masa molar como de la cantidad de sustancia."
        return run.evaluate(result)

    raise ValueError("Experimento sin ejecución implementada.")


def get_experiment(experiment_id: str) -> ExperimentSpec | None:
    return next((item for item in EXPERIMENT_SPECS if item.id == experiment_id), None)


def list_experiments() -> list[dict]:
    return [
        {
            "id": item.id, "title": item.title, "concept": item.concept,
            "hypothesis_prompt": item.hypothesis_prompt,
            "variables": list(item.variables), "steps": list(item.steps),
            "prediction_options": list(item.prediction_options),
            "controls": [c.serialize() for c in item.controls],
        } for item in EXPERIMENT_SPECS
    ]
