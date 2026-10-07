"""
reactions.py  ─  Átomos Perdidos v2
Puzles de reacción ("Camino de Reacción"): el jugador debe ordenar los
pasos de una reacción química real y responder una pregunta clave
(catalizador, condición, agente). La validación es pura (sin Flask)
para poder testearla de forma aislada.
"""

REACTIONS = [

    {
        "id": "agua",
        "titulo": "Síntesis del agua",
        "reactivos": "2 H₂ + O₂",
        "producto": "2 H₂O",
        "balance": {"reactants": ["H2", "O2"], "products": ["H2O"]},
        "dificultad": "Fácil",
        "descripcion": ("El hidrógeno y el oxígeno conviven tranquilos… hasta que "
                        "algo les da el empujón energético. Ordena los pasos para "
                        "sintetizar agua sin volar el laboratorio."),
        # Pasos en el ORDEN CORRECTO (se barajan al mostrarlos)
        "pasos": [
            "Mezclar H₂ y O₂ en proporción 2:1 en el reactor",
            "Aportar energía de activación con una chispa",
            "Reacción en cadena: los radicales H· y ·OH se combinan",
            "Condensar el vapor de H₂O formado",
        ],
        "pregunta": "¿Qué papel cumple la chispa en esta reacción?",
        "opciones": [
            "Aporta la energía de activación",
            "Actúa como catalizador",
            "Aumenta la presión del reactor",
            "Enfría los productos",
        ],
        "respuesta": 0,
        "puntos": 15,
        "fun_fact": ("Esta reacción liberó la energía que destruyó el dirigible "
                     "Hindenburg (1937) y es la misma que propulsa los cohetes "
                     "de hidrógeno líquido como el SLS de la NASA."),
    },

    {
        "id": "haber",
        "titulo": "Proceso Haber-Bosch (amoníaco)",
        "reactivos": "N₂ + 3 H₂",
        "producto": "2 NH₃",
        "balance": {"reactants": ["N2", "H2"], "products": ["NH3"]},
        "dificultad": "Media",
        "descripcion": ("Fijar el nitrógeno del aire alimenta a media humanidad. "
                        "Ordena los pasos del proceso industrial más importante "
                        "del siglo XX."),
        "pasos": [
            "Obtener N₂ del aire y H₂ del gas natural",
            "Comprimir la mezcla a ~200 atm y calentar a ~450 °C",
            "Pasar los gases por el lecho de catalizador de hierro",
            "Enfriar para licuar el NH₃ y recircular los gases sin reaccionar",
        ],
        "pregunta": "¿Qué catalizador se usa en el reactor?",
        "opciones": [
            "Hierro (Fe)",
            "Platino (Pt)",
            "Níquel (Ni)",
            "Vanadio (V₂O₅)",
        ],
        "respuesta": 0,
        "puntos": 20,
        "fun_fact": ("Sin el proceso Haber-Bosch no habría fertilizantes "
                     "nitrogenados suficientes: casi la mitad del nitrógeno de "
                     "tu cuerpo pasó alguna vez por uno de estos reactores."),
    },

    {
        "id": "vinagre",
        "titulo": "Del vino al vinagre (oxidación del etanol)",
        "reactivos": "C₂H₅OH + O₂",
        "producto": "CH₃COOH + H₂O",
        "balance": {"reactants": ["C2H5OH", "O2"], "products": ["CH3COOH", "H2O"]},
        "dificultad": "Media",
        "descripcion": ("Una botella de vino mal cerrada termina en vinagre. "
                        "Ordena los pasos de esta oxidación biológica de dos etapas."),
        "pasos": [
            "Partir de una disolución de etanol (vino o sidra)",
            "Exponer el líquido al oxígeno del aire",
            "Las bacterias Acetobacter oxidan el etanol a acetaldehído",
            "El acetaldehído se oxida a ácido acético: ya es vinagre",
        ],
        "pregunta": "¿Qué agente cataliza esta oxidación en dos etapas?",
        "opciones": [
            "Las bacterias del género Acetobacter",
            "Las levaduras Saccharomyces",
            "El dióxido de manganeso",
            "La luz ultravioleta",
        ],
        "respuesta": 0,
        "puntos": 20,
        "fun_fact": ("El intermediario, el acetaldehído, es el mismo compuesto "
                     "responsable de gran parte de la resaca: tu hígado hace esta "
                     "misma química con la enzima alcohol-deshidrogenasa."),
    },
]


def obtener_reaccion(reaction_id: str):
    """Devuelve el puzle con ese id, o None si no existe."""
    for r in REACTIONS:
        if r["id"] == reaction_id:
            return r
    return None


def listar_reacciones() -> list:
    """Resumen de todos los puzles (para la página de listado)."""
    return [{"id": r["id"], "titulo": r["titulo"], "reactivos": r["reactivos"],
             "producto": r["producto"], "dificultad": r["dificultad"],
             "puntos": r["puntos"], "balance": r.get("balance")} for r in REACTIONS]


def validar_reaccion(reaction_id: str, orden: list, respuesta: int) -> dict:
    """
    Valida la solución del jugador.
      orden     : lista de índices originales de los pasos, en el orden elegido.
                  La solución correcta es [0, 1, 2, ..., n-1].
      respuesta : índice de la opción elegida para la pregunta.
    """
    r = obtener_reaccion(reaction_id)
    if not r:
        return {"ok": False, "error": "Reacción desconocida."}

    n = len(r["pasos"])
    orden_ok = list(orden) == list(range(n))
    pregunta_ok = int(respuesta) == r["respuesta"]

    detalle = []
    if not orden_ok:
        detalle.append("El orden de los pasos no es correcto.")
    if not pregunta_ok:
        detalle.append("La respuesta a la pregunta no es correcta.")

    return {
        "ok": True,
        "correcto": orden_ok and pregunta_ok,
        "orden_ok": orden_ok,
        "pregunta_ok": pregunta_ok,
        "detalle": " ".join(detalle),
        "puntos": r["puntos"] if (orden_ok and pregunta_ok) else 0,
        "fun_fact": r["fun_fact"] if (orden_ok and pregunta_ok) else "",
    }
