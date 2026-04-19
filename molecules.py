"""
Moléculas y lógica del juego - Átomos Perdidos
Controlado completamente desde Python
"""

# ─────────────────────────────────────────────
# ESTRUCTURA DE CADA MOLÉCULA:
# name        : nombre español
# formula     : fórmula química con subíndices Unicode
# atoms       : lista de símbolos atómicos en orden
# missing     : índices (0-based) de los átomos que faltan
# hints       : 3 pistas basadas en conf. electrónica
# fun_fact    : curiosidad / aplicación real
# svg_key     : clave para el dibujo SVG (generado en app.py)
# ─────────────────────────────────────────────

MOLECULES = {
    "easy": [
        {
            "id": "H2",
            "name": "Hidrógeno molecular",
            "formula": "H₂",
            "atoms": ["H", "H"],
            "missing": [1],
            "hints": [
                "El átomo faltante tiene 1 electrón de valencia (capa s).",
                "Pertenece al Grupo 1, Período 1 de la tabla periódica.",
                "Su configuración electrónica completa es: 1s¹"
            ],
            "fun_fact": "El H₂ es el combustible más limpio del universo: al quemarse solo produce agua. Las estrellas como el Sol lo usan como fuente de energía mediante fusión nuclear.",
            "svg_key": "H2"
        },
        {
            "id": "O2",
            "name": "Oxígeno molecular",
            "formula": "O₂",
            "atoms": ["O", "O"],
            "missing": [0],
            "hints": [
                "El átomo faltante tiene 6 electrones de valencia.",
                "Pertenece al Grupo 16, Período 2 de la tabla periódica.",
                "Su configuración abreviada es: [He] 2s² 2p⁴"
            ],
            "fun_fact": "El O₂ representa el 21% de la atmósfera terrestre. Sin él, la vida aeróbica sería imposible. También se usa en hospitales y en la industria del acero.",
            "svg_key": "O2"
        },
        {
            "id": "N2",
            "name": "Nitrógeno molecular",
            "formula": "N₂",
            "atoms": ["N", "N"],
            "missing": [1],
            "hints": [
                "El átomo faltante tiene 5 electrones de valencia.",
                "Pertenece al Grupo 15, Período 2 de la tabla periódica.",
                "Su configuración abreviada es: [He] 2s² 2p³"
            ],
            "fun_fact": "El N₂ constituye el 78% del aire que respiramos. Su triple enlace covalente lo hace extremadamente estable. Se usa para conservar alimentos y enfriar semiconductores.",
            "svg_key": "N2"
        },
        {
            "id": "HCl",
            "name": "Ácido clorhídrico",
            "formula": "HCl",
            "atoms": ["H", "Cl"],
            "missing": [1],
            "hints": [
                "El átomo faltante tiene 7 electrones de valencia.",
                "Pertenece al Grupo 17 (halógenos), Período 3.",
                "Su configuración abreviada es: [Ne] 3s² 3p⁵"
            ],
            "fun_fact": "El HCl disuelto en agua forma el ácido clorhídrico, presente en el jugo gástrico del estómago. También es esencial en la industria química y en la limpieza de metales.",
            "svg_key": "HCl"
        },
        {
            "id": "F2",
            "name": "Flúor molecular",
            "formula": "F₂",
            "atoms": ["F", "F"],
            "missing": [0],
            "hints": [
                "El átomo faltante tiene 7 electrones de valencia y es el más electronegativo.",
                "Pertenece al Grupo 17 (halógenos), Período 2.",
                "Su configuración abreviada es: [He] 2s² 2p⁵"
            ],
            "fun_fact": "El F₂ es el elemento más electronegativo de toda la tabla periódica (3.98). Es tan reactivo que puede encender el vidrio o el agua. Se usa para producir PTFE (teflón).",
            "svg_key": "F2"
        },
        {
            "id": "NaCl",
            "name": "Cloruro de sodio",
            "formula": "NaCl",
            "atoms": ["Na", "Cl"],
            "missing": [0],
            "hints": [
                "El átomo faltante tiene 1 electrón de valencia en el orbital 3s.",
                "Pertenece al Grupo 1 (metales alcalinos), Período 3.",
                "Su configuración abreviada es: [Ne] 3s¹"
            ],
            "fun_fact": "El NaCl es la sal de mesa. Es un compuesto iónico esencial para la vida: regula la presión osmótica en las células. También se usa para conservar alimentos y en invierno para derretir hielo.",
            "svg_key": "NaCl"
        },
    ],

    "medium": [
        {
            "id": "H2O",
            "name": "Agua",
            "formula": "H₂O",
            "atoms": ["H", "H", "O"],
            "missing": [2],
            "hints": [
                "El átomo faltante tiene 6 electrones de valencia.",
                "Pertenece al Grupo 16, Período 2 de la tabla periódica.",
                "Su configuración abreviada es: [He] 2s² 2p⁴"
            ],
            "fun_fact": "El H₂O cubre el 71% de la Tierra. Su estructura angular (104.5°) le da propiedades únicas: alta tensión superficial, capacidad calorífica excepcional, y es el solvente universal de la vida.",
            "svg_key": "H2O"
        },
        {
            "id": "CO2",
            "name": "Dióxido de carbono",
            "formula": "CO₂",
            "atoms": ["C", "O", "O"],
            "missing": [0, 2],
            "hints": [
                "El átomo faltante (posición 1) tiene 4 electrones de valencia.",
                "Pertenece al Grupo 14, Período 2 de la tabla periódica.",
                "Su configuración abreviada es: [He] 2s² 2p²"
            ],
            "fun_fact": "El CO₂ es el gas responsable del efecto invernadero. Las plantas lo absorben en la fotosíntesis para producir glucosa y oxígeno. También es el gas de las burbujas en las bebidas carbonatadas.",
            "svg_key": "CO2"
        },
        {
            "id": "NH3",
            "name": "Amoníaco",
            "formula": "NH₃",
            "atoms": ["N", "H", "H", "H"],
            "missing": [1, 3],
            "hints": [
                "Los átomos faltantes tienen 1 electrón de valencia cada uno.",
                "Pertenecen al Grupo 1, Período 1.",
                "Su configuración electrónica completa es: 1s¹"
            ],
            "fun_fact": "El NH₃ es fundamental para la agricultura: es la base de los fertilizantes nitrogenados. Se produce industrialmente mediante el proceso Haber-Bosch, que 'fija' el nitrógeno del aire.",
            "svg_key": "NH3"
        },
        {
            "id": "CH4",
            "name": "Metano",
            "formula": "CH₄",
            "atoms": ["C", "H", "H", "H", "H"],
            "missing": [0],
            "hints": [
                "El átomo central tiene 4 electrones de valencia.",
                "Pertenece al Grupo 14, Período 2 de la tabla periódica.",
                "Su configuración abreviada es: [He] 2s² 2p²"
            ],
            "fun_fact": "El CH₄ es el componente principal del gas natural. También lo producen las vacas durante la digestión. En Titán (luna de Saturno) hay lagos y ríos de metano líquido.",
            "svg_key": "CH4"
        },
        {
            "id": "SO2",
            "name": "Dióxido de azufre",
            "formula": "SO₂",
            "atoms": ["S", "O", "O"],
            "missing": [0],
            "hints": [
                "El átomo central tiene 6 electrones de valencia y está en el período 3.",
                "Pertenece al Grupo 16, Período 3 de la tabla periódica.",
                "Su configuración abreviada es: [Ne] 3s² 3p⁴"
            ],
            "fun_fact": "El SO₂ se libera en las erupciones volcánicas y es un contaminante del aire. Se usa como conservante en vinos y frutas secas. Al reaccionar con agua forma lluvia ácida.",
            "svg_key": "SO2"
        },
        {
            "id": "H2S",
            "name": "Sulfuro de hidrógeno",
            "formula": "H₂S",
            "atoms": ["H", "H", "S"],
            "missing": [2],
            "hints": [
                "El átomo faltante tiene 6 electrones de valencia y está en el período 3.",
                "Pertenece al Grupo 16, Período 3 de la tabla periódica.",
                "Su configuración abreviada es: [Ne] 3s² 3p⁴"
            ],
            "fun_fact": "El H₂S huele a huevos podridos y es tóxico. Sin embargo, ciertos microorganismos en fuentes hidrotermales lo usan como fuente de energía en lugar de la luz solar.",
            "svg_key": "H2S"
        },
        {
            "id": "NO2",
            "name": "Dióxido de nitrógeno",
            "formula": "NO₂",
            "atoms": ["N", "O", "O"],
            "missing": [1],
            "hints": [
                "El átomo faltante tiene 6 electrones de valencia.",
                "Pertenece al Grupo 16, Período 2 de la tabla periódica.",
                "Su configuración abreviada es: [He] 2s² 2p⁴"
            ],
            "fun_fact": "El NO₂ es un gas tóxico de color marrón-rojizo producido por los motores de combustión. Es uno de los principales contaminantes urbanos y contribuye a la formación de smog fotoquímico.",
            "svg_key": "NO2"
        },
    ],

    "hard": [
        {
            "id": "H2SO4",
            "name": "Ácido sulfúrico",
            "formula": "H₂SO₄",
            "atoms": ["H", "H", "S", "O", "O", "O", "O"],
            "missing": [2, 3],
            "hints": [
                "El átomo en posición 3 tiene 6 electrones de valencia (período 3).",
                "Pertenece al Grupo 16, Período 3 de la tabla periódica.",
                "Su configuración abreviada es: [Ne] 3s² 3p⁴"
            ],
            "fun_fact": "El H₂SO₄ es el compuesto químico más producido del mundo. Se usa en la fabricación de fertilizantes, baterías de auto, y en la refinación de petróleo. Es extremadamente corrosivo.",
            "svg_key": "H2SO4"
        },
        {
            "id": "HNO3",
            "name": "Ácido nítrico",
            "formula": "HNO₃",
            "atoms": ["H", "N", "O", "O", "O"],
            "missing": [1, 4],
            "hints": [
                "El átomo faltante (pos. 2) tiene 5 electrones de valencia.",
                "Pertenece al Grupo 15, Período 2 de la tabla periódica.",
                "Su configuración abreviada es: [He] 2s² 2p³"
            ],
            "fun_fact": "El HNO₃ se usa para fabricar explosivos, fertilizantes y colorantes. La mezcla de HNO₃ y HCl (agua regia) puede disolver el oro y el platino, los metales más resistentes.",
            "svg_key": "HNO3"
        },
        {
            "id": "C2H5OH",
            "name": "Etanol",
            "formula": "C₂H₅OH",
            "atoms": ["C", "C", "H", "H", "H", "H", "H", "O", "H"],
            "missing": [0, 7],
            "hints": [
                "El átomo en pos. 1 tiene 4 electrones de valencia (Grupo 14, Período 2).",
                "El átomo en pos. 8 tiene 6 electrones de valencia (Grupo 16, Período 2).",
                "Sus configuraciones: C → [He] 2s² 2p²  |  O → [He] 2s² 2p⁴"
            ],
            "fun_fact": "El C₂H₅OH es el alcohol de bebidas fermentadas. Se produce por fermentación de azúcares con levaduras. También es combustible renovable: Brasil produce gasolina con 27% de etanol de caña de azúcar.",
            "svg_key": "C2H5OH"
        },
        {
            "id": "CH3COOH",
            "name": "Ácido acético",
            "formula": "CH₃COOH",
            "atoms": ["C", "H", "H", "H", "C", "O", "O", "H"],
            "missing": [0, 5],
            "hints": [
                "Ambos átomos faltantes son del mismo elemento del Grupo 14, Período 2.",
                "Tienen 4 electrones de valencia cada uno.",
                "Su configuración abreviada es: [He] 2s² 2p²"
            ],
            "fun_fact": "El CH₃COOH es el ácido del vinagre (5-8% de concentración). También es fundamental en bioquímica: la coenzima A transporta grupos acetilo en el metabolismo energético.",
            "svg_key": "CH3COOH"
        },
        {
            "id": "NaOH",
            "name": "Hidróxido de sodio",
            "formula": "NaOH",
            "atoms": ["Na", "O", "H"],
            "missing": [1, 2],
            "hints": [
                "El átomo en pos. 2 tiene 6 electrones de valencia (Grupo 16, Período 2).",
                "El átomo en pos. 3 tiene 1 electrón de valencia (Grupo 1, Período 1).",
                "Configuraciones: O → [He] 2s² 2p⁴  |  H → 1s¹"
            ],
            "fun_fact": "El NaOH (soda cáustica) es una base muy fuerte usada en jabones, papel, y tratamiento de aguas. Es tan corrosiva que puede disolver tejido orgánico. Se produce electrolizando salmuera.",
            "svg_key": "NaOH"
        },
        {
            "id": "MgCl2",
            "name": "Cloruro de magnesio",
            "formula": "MgCl₂",
            "atoms": ["Mg", "Cl", "Cl"],
            "missing": [0],
            "hints": [
                "El átomo central tiene 2 electrones de valencia.",
                "Pertenece al Grupo 2 (metales alcalinotérreos), Período 3.",
                "Su configuración abreviada es: [Ne] 3s²"
            ],
            "fun_fact": "El MgCl₂ es abundante en el agua de mar. Se usa para fabricar tofu (coagulante), como suplemento deportivo, y para derretir hielo en carreteras a bajas temperaturas.",
            "svg_key": "MgCl2"
        },
        {
            "id": "CaCO3",
            "name": "Carbonato de calcio",
            "formula": "CaCO₃",
            "atoms": ["Ca", "C", "O", "O", "O"],
            "missing": [1, 4],
            "hints": [
                "El átomo en pos. 2 tiene 4 electrones de valencia (Grupo 14, Período 2).",
                "El átomo en pos. 5 tiene 6 electrones de valencia (Grupo 16, Período 2).",
                "Configuraciones: C → [He] 2s² 2p²  |  O → [He] 2s² 2p⁴"
            ],
            "fun_fact": "El CaCO₃ forma el mármol, la caliza y las conchas marinas. Es el principal componente del cemento. También es antiácido estomacal. Los corales están hechos de CaCO₃.",
            "svg_key": "CaCO3"
        },
    ]
}

# ─────────────────────────────────────────────
# LÓGICA DEL JUEGO
# ─────────────────────────────────────────────

class GameSession:
    """Controla el estado de una partida de un jugador."""

    MAX_HINTS = 3

    def __init__(self, level: str):
        if level not in MOLECULES:
            raise ValueError(f"Nivel '{level}' no válido. Use: easy, medium, hard")
        self.level = level
        self.molecules = MOLECULES[level]
        self.current_index = 0
        self.score = 0
        self.hints_used = 0
        self.attempts = 0

    # ── Consultas ──────────────────────────────
    @property
    def current_molecule(self):
        if self.current_index < len(self.molecules):
            return self.molecules[self.current_index]
        return None

    @property
    def is_finished(self):
        return self.current_index >= len(self.molecules)

    @property
    def hints_remaining(self):
        return self.MAX_HINTS - self.hints_used

    def get_display_atoms(self):
        """Retorna los átomos con los faltantes enmascarados como '?'."""
        mol = self.current_molecule
        if not mol:
            return []
        return [
            {"symbol": "?", "missing": True, "index": i}
            if i in mol["missing"]
            else {"symbol": sym, "missing": False, "index": i}
            for i, sym in enumerate(mol["atoms"])
        ]

    # ── Acciones ──────────────────────────────
    def request_hint(self):
        """Solicita la siguiente pista disponible."""
        mol = self.current_molecule
        if not mol:
            return {"ok": False, "msg": "No hay molécula activa."}
        if self.hints_used >= self.MAX_HINTS:
            return {"ok": False, "msg": "Ya usaste todas las pistas."}
        hint_text = mol["hints"][self.hints_used]
        self.hints_used += 1
        return {
            "ok": True,
            "hint": hint_text,
            "hint_number": self.hints_used,
            "remaining": self.hints_remaining
        }

    def submit_answer(self, slot_index: int, element_symbol: str):
        """
        Verifica si el elemento colocado en slot_index es correcto.
        Retorna dict con resultado.
        """
        mol = self.current_molecule
        if not mol:
            return {"ok": False, "correct": False, "msg": "No hay molécula activa."}
        if slot_index not in mol["missing"]:
            return {"ok": False, "correct": False, "msg": "Ese hueco no existe."}

        expected = mol["atoms"][slot_index]
        self.attempts += 1

        if element_symbol.strip().capitalize() == expected:
            return {"ok": True, "correct": True, "expected": expected}
        else:
            return {
                "ok": True,
                "correct": False,
                "expected": expected,
                "msg": f"Incorrecto. '{element_symbol}' no es el átomo esperado en esa posición."
            }

    def check_molecule_complete(self, filled: dict) -> bool:
        """
        filled: {slot_index: symbol}
        Retorna True si todos los huecos están correctamente llenos.
        """
        mol = self.current_molecule
        if not mol:
            return False
        for idx in mol["missing"]:
            if filled.get(idx, "").strip().capitalize() != mol["atoms"][idx]:
                return False
        return True

    def complete_molecule(self):
        """
        Avanza a la siguiente molécula y calcula puntuación.
        """
        points = max(10 - self.hints_used * 3, 1)
        self.score += points
        self.current_index += 1
        self.hints_used = 0
        self.attempts = 0
        return {"points_earned": points, "total_score": self.score}

    def reset(self):
        self.current_index = 0
        self.score = 0
        self.hints_used = 0
        self.attempts = 0


# ─── Helpers para la API ──────────────────────
def get_molecule_list(level: str) -> list:
    """Retorna lista ligera de moléculas para un nivel."""
    return [
        {"id": m["id"], "name": m["name"], "formula": m["formula"]}
        for m in MOLECULES.get(level, [])
    ]

def get_molecule_by_id(mol_id: str) -> dict | None:
    for level_mols in MOLECULES.values():
        for m in level_mols:
            if m["id"] == mol_id:
                return m
    return None

LEVEL_LABELS = {
    "easy":   "Fácil",
    "medium": "Medio",
    "hard":   "Difícil",
}
