"""
achievements.py  ─  Átomos Perdidos v2
Sistema de logros simple, persistido en la sesión de Flask.
La comprobación es una función pura sobre el estado de sesión + el evento,
para poder testearla sin servidor.
"""

LOGROS = {
    "primera_molecula": {
        "nombre": "Primera molécula",
        "desc": "Completa tu primera molécula",
        "emoji": "🧪",
    },
    "sin_pistas": {
        "nombre": "Sin pistas",
        "desc": "Completa una molécula sin usar ninguna pista",
        "emoji": "🧠",
    },
    "coleccionista": {
        "nombre": "Coleccionista",
        "desc": "Reúne 5 moléculas en la galería",
        "emoji": "📦",
    },
    "alquimista": {
        "nombre": "Alquimista",
        "desc": "Reúne 10 moléculas en la galería",
        "emoji": "⚗️",
    },
    "rey_sandbox": {
        "nombre": "Rey del Sandbox",
        "desc": "Guarda 5 moléculas creadas en el sandbox",
        "emoji": "👑",
    },
}


def comprobar_logros(desbloqueados: list, galeria: list, evento: dict) -> list:
    """
    Devuelve la lista de ids de logros NUEVOS según el estado actual.

    desbloqueados : ids ya obtenidos (de session["achievements"])
    galeria       : lista de entradas de session["gallery"]
    evento        : dict opcional con datos del momento, p. ej.
                    {"molecula_completada": True, "hints_usados": 0}
    """
    evento = evento or {}
    nuevos = []

    n_desafio = sum(1 for g in galeria if g.get("tipo") == "desafio")
    n_sandbox = sum(1 for g in galeria if g.get("tipo") == "sandbox")
    n_total = len(galeria)

    def _intentar(logro_id, condicion):
        if condicion and logro_id not in desbloqueados and logro_id not in nuevos:
            nuevos.append(logro_id)

    _intentar("primera_molecula", evento.get("molecula_completada") or n_desafio >= 1)
    _intentar("sin_pistas", evento.get("molecula_completada")
              and evento.get("hints_usados", 99) == 0)
    _intentar("coleccionista", n_total >= 5)
    _intentar("alquimista", n_total >= 10)
    _intentar("rey_sandbox", n_sandbox >= 5)

    return nuevos


def texto_toast(logro_id: str) -> str:
    """Texto del toast que anuncia el logro (lo dice Octeto)."""
    logro = LOGROS.get(logro_id)
    if not logro:
        return ""
    return f"🐙 ¡LOGRO DESBLOQUEADO! {logro['emoji']} {logro['nombre']} — {logro['desc']}"
