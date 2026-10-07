"""Currículo progresivo de Átomos Perdidos.

La dificultad deja de depender exclusivamente de easy/medium/hard. Cada etapa
combina conocimientos nuevos con modos de problema progresivamente más abiertos.
"""

STAGES = [
    {"id": 0, "name": "El átomo", "domain": "atomos", "requires": [],
     "modes": ["identify"], "goal": "Reconocer estructura atómica y símbolos."},
    {"id": 1, "name": "La tabla", "domain": "tabla_periodica", "requires": [0],
     "modes": ["identify", "lookup"], "goal": "Leer grupos, períodos y electrones de valencia."},
    {"id": 2, "name": "Los enlaces", "domain": "enlaces", "requires": [1],
     "modes": ["complete", "identify"], "goal": "Distinguir enlaces iónicos y covalentes."},
    {"id": 3, "name": "Construcción molecular", "domain": "moleculas", "requires": [2],
     "modes": ["complete", "build"], "goal": "Construir moléculas a partir de sus átomos."},
    {"id": 4, "name": "Forma y espacio", "domain": "geometria", "requires": [3],
     "modes": ["identify", "predict"], "goal": "Relacionar pares electrónicos con geometría VSEPR."},
    {"id": 5, "name": "Cantidad de materia", "domain": "formulas", "requires": [3],
     "modes": ["formula", "mass"], "goal": "Interpretar fórmulas y composición."},
    {"id": 6, "name": "Transformaciones", "domain": "reacciones", "requires": [4, 5],
     "modes": ["sequence", "balance", "predict"], "goal": "Comprender y balancear reacciones."},
    {"id": 7, "name": "Química orgánica", "domain": "organica", "requires": [6],
     "modes": ["identify", "build", "transform"], "goal": "Reconocer familias y transformaciones orgánicas."},
    {"id": 8, "name": "Laboratorio", "domain": "laboratorio", "requires": [7],
     "modes": ["experiment", "investigate"], "goal": "Resolver problemas abiertos mediante experimentación."},
]

def knowledge_tree() -> list[dict]:
    return [dict(stage) for stage in STAGES]
