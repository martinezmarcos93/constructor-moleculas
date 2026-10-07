"""Campaña científica de Átomos Perdidos.

Orquesta progresión, misiones y descubrimientos sin duplicar reglas químicas.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class CampaignChapter:
    id: str
    title: str
    briefing: str
    domain: str
    requires_mastery: int
    mission_templates: tuple[str, ...]
    reward_xp: int
    reward_credits: int
    narrative: str

    def serialize(self) -> dict:
        return asdict(self)


CHAPTERS = (
    CampaignChapter("capitulo-1", "La señal perdida", "Recupera el control del laboratorio.", "atomos", 0, ("fabrica_agua",), 15, 2, "Los instrumentos vuelven a responder. La señal contiene una fórmula."),
    CampaignChapter("capitulo-2", "El mapa de los elementos", "Aprende a leer el mapa periódico.", "tabla_periodica", 25, ("fabrica_agua",), 20, 3, "La tabla se convierte en un mapa de propiedades."),
    CampaignChapter("capitulo-3", "Arquitectos de enlaces", "Haz encajar fragmentos respetando sus valencias.", "enlaces", 25, ("fabrica_agua",), 25, 4, "Descubres que la estructura nace de los enlaces."),
    CampaignChapter("capitulo-4", "La cámara molecular", "Construye estructuras estables y descubre su geometría.", "moleculas", 25, ("fabrica_agua",), 30, 5, "Una molécula desconocida aparece en el visor."),
    CampaignChapter("capitulo-5", "Materia bajo presión", "Calcula cuánto material necesitas.", "formulas", 25, ("fabrica_agua", "planta_amoniaco"), 40, 7, "Cada recurso desperdiciado tiene un coste."),
    CampaignChapter("capitulo-6", "El reactor", "Balancea, predice y produce sin desperdicio.", "reacciones", 25, ("fabrica_agua", "planta_amoniaco"), 50, 10, "Has dejado de resolver ejercicios: ahora diriges un reactor."),
    CampaignChapter("capitulo-7", "Laboratorio abierto", "Diseña, prueba y optimiza estrategias.", "laboratorio", 60, ("fabrica_agua", "planta_amoniaco"), 75, 15, "El laboratorio deja de decirte qué hacer."),
)


def campaign_snapshot(progression: dict | None) -> dict:
    mastery = (progression or {}).get("mastery", {})
    chapters = []
    for chapter in CHAPTERS:
        value = int(mastery.get(chapter.domain, {}).get("value", 0))
        chapters.append({**chapter.serialize(), "mastery": value, "unlocked": value >= chapter.requires_mastery})
    return {"chapters": chapters}


def current_chapter(progression: dict | None) -> dict:
    chapters = campaign_snapshot(progression)["chapters"]
    unlocked = [chapter for chapter in chapters if chapter["unlocked"]]
    return unlocked[-1] if unlocked else chapters[0]


def reward_for_chapter(chapter_id: str) -> dict:
    for chapter in CHAPTERS:
        if chapter.id == chapter_id:
            return {"xp": chapter.reward_xp, "credits": chapter.reward_credits}
    raise ValueError("Capítulo desconocido.")
