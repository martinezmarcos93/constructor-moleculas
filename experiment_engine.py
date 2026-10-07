"""Motor mínimo de experimentos para el laboratorio.

Un experimento educativo declara hipótesis, variables y resultado esperado.
No simula todavía cinética o termodinámica: prepara el contrato para hacerlo.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Experiment:
    id: str
    title: str
    hypothesis_prompt: str
    variables: tuple[str, ...]
    steps: tuple[str, ...]
    observations: list[str] = field(default_factory=list)

    def record_observation(self, observation: str) -> None:
        observation = observation.strip()
        if observation:
            self.observations.append(observation)

    def report(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "hypothesis_prompt": self.hypothesis_prompt,
            "variables": list(self.variables),
            "steps": list(self.steps),
            "observations": list(self.observations),
            "completed": bool(self.observations),
        }


EXPERIMENTS = (
    Experiment(
        "polaridad_agua",
        "¿Por qué el agua se comporta como molécula polar?",
        "Predice si la geometría de H₂O permite cancelar sus dipolos.",
        ("estructura", "geometría", "electronegatividad"),
        ("Construye H₂O.", "Valida su geometría.", "Compara la electronegatividad O-H.", "Formula una explicación."),
    ),
    Experiment(
        "conservacion_materia",
        "¿Se conservan los átomos durante una reacción?",
        "Predice si el número de átomos de cada elemento puede cambiar.",
        ("reactivos", "productos", "coeficientes"),
        ("Elige una reacción.", "Balancea los coeficientes.", "Compara átomos a ambos lados.", "Registra tu conclusión."),
    ),
)


def get_experiment(experiment_id: str) -> Experiment | None:
    for experiment in EXPERIMENTS:
        if experiment.id == experiment_id:
            return Experiment(
                experiment.id,
                experiment.title,
                experiment.hypothesis_prompt,
                experiment.variables,
                experiment.steps,
            )
    return None


def list_experiments() -> list[dict]:
    return [experiment.report() for experiment in EXPERIMENTS]
