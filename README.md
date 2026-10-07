# ⚗️ Átomos Perdidos: El Constructor de Moléculas

Juego educativo web construido **100% en Python** con Flask.
El HTML, CSS, la tabla periódica, los SVG de moléculas y toda la lógica
del juego se generan dinámicamente desde Python.

> 🐙 **Versión 2**: asistente Octeto, visor 3D, modo sandbox, puzles de
> reacción, galería, logros y misión narrativa.
> Ver [README_MEJORAS.md](README_MEJORAS.md).

---

## 🚀 Instalación y arranque

```bash
# 1. Instalar dependencias (solo Flask)
pip install -r requirements.txt

# 2. Arrancar el servidor y abrir el navegador
python start.py

# Para detenerlo
python stop.py

# 3. Abrir en el navegador
http://localhost:5000
```

---

## 📁 Estructura del proyecto

```
atomos_perdidos/
├── app.py              ← Servidor Flask + generación HTML desde Python
├── periodic_table.py   ← 118 elementos con todos sus datos
├── molecules.py        ← 63 moléculas + lógica de GameSession
├── svg_molecules.py    ← Diagramas SVG generados desde Python
├── octeto.py           ← Frases del asistente Octeto 🐙 (v2)
├── ui_common.py        ← Widgets compartidos: Octeto, toasts, sonidos, modal 3D (v2)
├── molecule_3d.py      ← Geometrías VSEPR → formato XYZ para 3Dmol.js (v2)
├── chemistry_rules.py  ← Reglas didácticas de fórmulas y valencias
├── molecular_structure.py ← Grafo explícito de átomos + enlaces
├── vsepr.py             ← Geometría molecular introductoria
├── stoichiometry.py     ← Fórmulas, masa molar y composición
├── reaction_engine.py   ← Balanceo por conservación de átomos
├── reactions.py        ← Puzles de reacción + validación (v2)
├── missions.py         ← Misión narrativa "El Elixir de la Vida" (v2)
├── achievements.py     ← Sistema de logros (v2)
├── views_nuevas.py     ← Páginas nuevas: sandbox, galería, reacciones… (v2)
├── progression.py       ← Maestría y desbloqueos pedagógicos
├── challenge_model.py   ← Generación de desafíos por conceptos
├── adaptive_tutor.py    ← Tutor Octeto adaptativo
├── tests/                ← Pruebas unitarias del núcleo
├── requirements.txt
├── README.md
└── README_MEJORAS.md   ← Detalle de las novedades v2
```

---

## 🎮 Cómo jugar

1. Elige un nivel: **Fácil**, **Medio** o **Difícil**
2. Observa la molécula con átomos faltantes (`?`)
3. Haz clic en un hueco `?` para activarlo
4. Haz clic en el elemento correcto en la **Tabla Periódica**
5. Pulsa **⚗️ Colocar en hueco**
6. Si no sabes, pide hasta **3 pistas** basadas en configuración electrónica
7. Al completar la molécula, ves su estructura SVG y una curiosidad

---

## 🔬 Características técnicas

### Python controla todo:
- `periodic_table.py` define los 118 elementos: símbolo, nombre, masa,
  configuración electrónica, electrones de valencia, electronegatividad,
  estado, categoría, grupo y período.
- `molecules.py` contiene la clase `GameSession` que gestiona el estado
  de la partida, las pistas y la puntuación.
- `svg_molecules.py` genera los diagramas SVG de cada molécula
  calculando posiciones de átomos y enlaces con Python (math).
- `app.py` genera el HTML completo de cada página con f-strings Python,
  incluida la tabla periódica en formato grid CSS.

### Moléculas incluidas:

| Nivel | Moléculas |
|-------|-----------|
| Fácil | H₂, O₂, N₂, F₂, HCl, NaCl |
| Medio | H₂O, CO₂, NH₃, CH₄, SO₂, H₂S, NO₂ |
| Difícil | H₂SO₄, HNO₃, C₂H₅OH, CH₃COOH, NaOH, MgCl₂, CaCO₃ |

### Sistema de pistas (basado en configuración electrónica):
- **Pista 1**: Número de electrones de valencia
- **Pista 2**: Grupo y período en la tabla periódica
- **Pista 3**: Configuración electrónica abreviada completa

### Puntuación:
- 10 pts sin pistas
- 7 pts con 1 pista
- 4 pts con 2 pistas
- 1 pt  con 3 pistas

---

## 🧪 Constructor químico

El Sandbox ya trabaja con una representación explícita de estructura: átomos,
enlaces simples/dobles/triples, valencia y conectividad. La validación se
realiza en servidor y el frontend muestra si la estructura es válida y, cuando
corresponde, su geometría VSEPR. También existen APIs para masa molar,
composición porcentual, polaridad, balanceo de ecuaciones y experimentos educativos.

El motor es deliberadamente educativo: una estructura marcada como válida
significa que satisface las reglas didácticas implementadas, no que constituya
una predicción química profesional para cualquier compuesto.

## 🔧 Extensión del juego

Para añadir nuevas moléculas, edita `molecules.py`:

```python
{
    "id": "H2O2",
    "name": "Peróxido de hidrógeno",
    "formula": "H₂O₂",
    "atoms": ["H", "O", "O", "H"],
    "missing": [1, 2],          # índices de los átomos que faltan
    "hints": [
        "Los átomos faltantes tienen 6 electrones de valencia.",
        "Pertenecen al Grupo 16, Período 2.",
        "Configuración: [He] 2s² 2p⁴"
    ],
    "fun_fact": "El H₂O₂ es el agua oxigenada...",
    "svg_key": "H2O2"          # define svg_H2O2() en svg_molecules.py
}
```

Para añadir su SVG, agrega en `svg_molecules.py`:

```python
def svg_H2O2():
    s  = _bond(30, 60, 80, 60)
    s += _bond(80, 60, 130, 60)
    s += _bond(130, 60, 180, 60)
    s += _atom(30, 60, "H")
    s += _atom(80, 60, "O")
    s += _atom(130, 60, "O")
    s += _atom(180, 60, "H")
    return _wrap(s, 210, 120)

SVG_REGISTRY["H2O2"] = svg_H2O2
```

---

## 🌐 API REST (para desarrolladores)

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/elements` | GET | JSON con los 118 elementos |
| `/api/molecules` | GET | JSON con todas las moléculas |
| `/game/<level>/play` | GET | Página del juego en curso |
| `/place_element` | POST | Colocar átomo en hueco |
| `/hint` | POST | Pedir pista |
| `/next_molecule` | POST | Avanzar a siguiente molécula |
| `/clear_slot` | POST | Borrar átomo colocado |
| `/api/structure/validate` | POST | Validar átomos, enlaces y VSEPR |
| `/api/stoichiometry/analyze` | POST | Masa molar y composición |
| `/api/reaction/balance` | POST | Balancear una ecuación química |
| `/api/polarity/analyze` | POST | Analizar polaridad de enlaces/estructuras |
| `/api/experiments` | GET | Catálogo de experimentos del laboratorio |


### Experimentos jugables

El laboratorio ya dispone de un motor de experimentos con cuatro etapas:
**predicción → ejecución → observación → evaluación**.

Cada experimento puede declarar conceptos, variables, opciones de predicción,
pasos y resultado calculado. La API `/api/experiments/<id>/run` devuelve el
resultado químico y una puntuación educativa. Actualmente existen experimentos
sobre polaridad de H₂O, conservación de la materia y masa molar.

La puntuación no evalúa solamente acertar: registrar una observación forma parte
del experimento. Esto prepara el sistema para introducir hipótesis, variables
controlables, evidencias y conclusiones en futuras misiones.


Los experimentos incorporan ahora **variables manipulables** y límites didácticos.
El jugador puede cambiar cantidades de reactivos, cantidades de sustancia o
condiciones registradas, ejecutar el experimento y recibir evidencia calculada.
La intención es que la pregunta pase de «¿cuál es la respuesta?» a
«¿qué ocurre si modifico esta variable?».


El laboratorio de reacciones permite seleccionar una reacción educativa, modificar
las cantidades iniciales de los reactivos y calcular automáticamente el balance,
el reactivo limitante, los reactivos en exceso y el rendimiento teórico en moles.
La misma mecánica puede reutilizarse en misiones donde el jugador deba optimizar
recursos o elegir proporciones de reactivos.
