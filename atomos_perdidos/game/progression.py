from __future__ import annotations
"""Modelo mínimo de progresión y dominio de conocimiento."""
from __future__ import annotations
from dataclasses import dataclass, field

DOMAINS = ("atomos", "tabla_periodica", "enlaces", "moleculas", "geometria", "formulas", "reacciones", "laboratorio", "organica")

@dataclass
class Mastery:
    value: int = 0
    attempts: int = 0
    correct: int = 0
    streak: int = 0
    def register(self, correct: bool, points: int = 1) -> None:
        self.attempts += 1
        if correct:
            self.correct += 1
            self.streak += 1
            self.value = min(100, self.value + max(1, points))
        else:
            self.streak = 0
            self.value = max(0, self.value - 1)

@dataclass
class Progression:
    mastery: dict[str, Mastery] = field(default_factory=lambda: {d: Mastery() for d in DOMAINS})
    def register(self, domain: str, correct: bool, points: int = 1) -> None:
        if domain not in self.mastery:
            raise ValueError(f"Dominio desconocido: {domain}")
        self.mastery[domain].register(correct, points)
    def unlocked_domains(self) -> list[str]:
        unlocked = ["atomos", "tabla_periodica"]
        gates = [("tabla_periodica", "enlaces", 25), ("enlaces", "moleculas", 25),
                 ("moleculas", "geometria", 25), ("geometria", "formulas", 25),
                 ("formulas", "reacciones", 25), ("reacciones", "laboratorio", 60), ("reacciones", "organica", 40)]
        for source, target, threshold in gates:
            if self.mastery[source].value >= threshold and target not in unlocked:
                unlocked.append(target)
        return unlocked
    def snapshot(self) -> dict:
        return {"mastery": {d: vars(s).copy() for d, s in self.mastery.items()},
                "unlocked": self.unlocked_domains()}

def load_progression(data: dict | None) -> Progression:
    p = Progression()
    if not isinstance(data, dict):
        return p
    for domain, values in data.get("mastery", {}).items():
        if domain not in p.mastery or not isinstance(values, dict):
            continue
        state = p.mastery[domain]
        state.value = max(0, min(100, int(values.get("value", 0))))
        state.attempts = max(0, int(values.get("attempts", 0)))
        state.correct = max(0, int(values.get("correct", 0)))
        state.streak = max(0, int(values.get("streak", 0)))
    return p
