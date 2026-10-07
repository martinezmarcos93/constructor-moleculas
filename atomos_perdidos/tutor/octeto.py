"""
octeto.py  ─  Átomos Perdidos v2
Octeto 🐙: el pulpo asistente del juego. Ocho brazos, cero paciencia
para los gases nobles. Devuelve frases ingeniosas según el evento.

Uso:
    from octeto import get_octeto_message
    msg = get_octeto_message("pista_usada", {"numero": 1, "pista": "..."})
"""

import random

# Frases por tipo de evento. Cuando hay varias, se elige una al azar
# para que Octeto no suene a disco rayado.
FRASES = {

    "bienvenida": [
        "¡Hola! Soy Octeto, tu pulpo de laboratorio. Ocho brazos, ocho electrones… ¿casualidad? No lo creo.",
        "¡Bienvenido al laboratorio! Yo soy Octeto. Si algo explota, fue el becario.",
        "Soy Octeto 🐙. Los gases nobles no me hablan, pero tú y yo vamos a construir maravillas.",
    ],

    "elemento_colocado": [
        "¡Ese átomo encajó como tentáculo en ventosa!",
        "¡Bien ahí! La regla del octeto estaría orgullosa (yo también, obvio).",
        "¡Plop! Sonido oficial de un enlace bien hecho.",
        "Un electrón compartido es un electrón feliz. ¡Sigue así!",
    ],

    "elemento_incorrecto": [
        "Mmm… ese átomo no va ahí. Confía en mí: tengo ocho brazos y ninguno lo señalaba.",
        "¡Casi! Pero la química es exigente. Mira la configuración electrónica de la pista.",
        "Ese elemento se ofendió y volvió a la tabla. Prueba con otro.",
    ],

    "error_valencia": [
        "¡Ojo! Las valencias no cuadran. Ese enlace aguanta menos que yo sin cafeína.",
        "Hmm, ese átomo ya no tiene electrones libres para compartir. ¡No lo agobies!",
        "La valencia manda: no puedes colgar más enlaces ahí. Créeme, lo intenté con mis tentáculos.",
    ],

    "molecula_completa": [
        "¡MOLÉCULA COMPLETA! *agita los ocho brazos a la vez*",
        "¡Lo lograste! Esto merece confeti. Y yo nunca desperdicio confeti.",
        "¡Enlace perfecto! Si tuviera manos, aplaudiría. Tengo algo mejor: ¡ocho tentáculos!",
        "¡Química pura! Hasta el flúor está impresionado, y eso que es muy electronegativo.",
    ],

    "nivel_completado": [
        "¡Nivel terminado! Ve a la galería a admirar tu colección, coleccionista de moléculas.",
        "¡Todas las moléculas completadas! Me quedé sin tinta de la emoción.",
    ],

    "sandbox_libertad": [
        "¡Aquí no hay reglas! Pero si rompes algo, yo no he sido…",
        "Modo sandbox: donde la valencia es más una sugerencia que una ley. ¡Crea con libertad!",
        "¡Libertad creativa! Frankenstein también empezó así, pero tú seguro lo haces mejor.",
    ],

    "sandbox_sin_valencia": [
        "Ese enlace viola la valencia… pero aquí mando poco. ¡Tú sabrás lo que haces! 😅",
        "En un examen eso sería incorrecto. Aquí es 'arte experimental'.",
    ],

    "galeria": [
        "Tu vitrina de trofeos moleculares. Cada una me costó una tinta de la emoción.",
        "¡Mira esa colección! Ni el museo de química de mi abuela pulpo tenía tantas.",
    ],

    "galeria_vacia": [
        "La galería está más vacía que la capa de valencia del helio… ¡Ve a completar moléculas!",
    ],

    "logro": [
        "¡LOGRO DESBLOQUEADO! Esto va directo a tu vitrina.",
        "¡Toma ya! Un logro nuevo. Lo celebraría con las ocho manos si no estuviera sujetando el matraz.",
    ],

    "reaccion_intro": [
        "Las reacciones son como recetas: el orden de los pasos SÍ altera el producto.",
        "Puzles de reacción: aquí no basta con qué, también importa el cómo y el cuándo.",
    ],

    "reaccion_correcta": [
        "¡Reacción completada! Estequiometría de campeonato.",
        "¡Eso es! Lavoisier estaría tomando notas ahora mismo.",
    ],

    "reaccion_incorrecta": [
        "Esa secuencia haría llorar a un catalizador. ¡Revisa el orden!",
        "Casi, pero esa reacción no ocurre así ni con toda la energía de activación del mundo.",
    ],

    "historia": [
        "Ponte cómodo, que esta historia tiene más química que un laboratorio en viernes.",
    ],

    "despedida": [
        "¡Hasta la próxima! Voy a reordenar mi colección de electrones.",
    ],
}

# Pistas: el mensaje depende del número de pista pedida (1, 2 o 3).
FRASES_PISTA = {
    1: "¡Agarra uno de mis tentáculos! Pista número 1: {pista}",
    2: "Vale, vale, no te estreses… Pista número 2: {pista}",
    3: "Esta es la última, ¿eh? Después estás solo… Pista número 3: {pista}",
}


def get_octeto_message(tipo: str, contexto: dict = None) -> str:
    """
    Devuelve una frase de Octeto (con su 🐙) para el evento dado.

    tipo      : clave de FRASES, o "pista_usada".
    contexto  : dict opcional. Para "pista_usada" espera:
                {"numero": 1|2|3, "pista": "texto de la pista"}
    """
    contexto = contexto or {}

    if tipo == "pista_usada":
        numero = min(max(int(contexto.get("numero", 1)), 1), 3)
        plantilla = FRASES_PISTA[numero]
        return "🐙 " + plantilla.format(pista=contexto.get("pista", ""))

    frases = FRASES.get(tipo)
    if not frases:
        # Evento desconocido: Octeto improvisa en vez de callar.
        return "🐙 *burbujea pensativo*"
    return "🐙 " + random.choice(frases)
