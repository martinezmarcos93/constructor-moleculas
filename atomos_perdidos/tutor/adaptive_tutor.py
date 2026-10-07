"""Tutor adaptativo de Octeto.

La regla es simple: cuanto mayor es la maestría, menos directa debe ser la ayuda.
"""
from __future__ import annotations

def help_level(mastery: int) -> str:
    if mastery < 25:
        return "direct"
    if mastery < 60:
        return "conceptual"
    if mastery < 85:
        return "guided"
    return "socratic"

def adapt(event: str, mastery: int, detail: str = "") -> str:
    level = help_level(mastery)
    if event == "wrong":
        if level == "direct":
            return f"🐙 Mira la pista concreta: {detail}"
        if level == "conceptual":
            return f"🐙 No te doy el elemento. Busca qué propiedad periódica decide este problema. {detail}"
        if level == "guided":
            return "🐙 Revisa electrones de valencia y grupo antes de cambiar tu respuesta."
        return "🐙 ¿Qué evidencia de la tabla periódica contradice tu elección?"
    if event == "success":
        if level in {"direct", "conceptual"}:
            return "🐙 Correcto. Fíjate ahora en qué propiedad hizo posible la solución."
        if level == "guided":
            return "🐙 Correcto. Intenta explicar el patrón antes de continuar."
        return "🐙 Correcto. Ahora justifícalo sin mirar la pista."
    return "🐙 Observa el patrón y formula una hipótesis antes de probar."

def tutor_message(event: str, progression: dict | None, domain: str, detail: str = "") -> str:
    mastery = 0
    if isinstance(progression, dict):
        mastery = int(progression.get("mastery", {}).get(domain, {}).get("value", 0))
    return adapt(event, mastery, detail)
