# ⚗️ Átomos Perdidos v2 — Novedades

Esta versión amplía el juego original manteniendo su filosofía: **todo el HTML,
CSS y JavaScript se genera desde Python** con f-strings. Nada del juego original
cambió de contrato; las rutas viejas siguen funcionando igual.

---

## 🐙 Octeto, el asistente del juego

Un pulpo de laboratorio con ocho brazos (y opiniones) que acompaña al jugador
en **todas las páginas** mediante un bocadillo flotante no intrusivo (en móvil
se compacta; se puede cerrar y reabrir tocando el 🐙).

- Reacciona al colocar átomos, equivocarse, completar moléculas y desbloquear logros.
- Sistema de pistas con personalidad: la 1ª («¡Agarra uno de mis tentáculos!»),
  la 2ª («Vale, vale, no te estreses…») y la 3ª («Esta es la última, ¿eh?»).
- Módulo: `octeto.py` → `get_octeto_message(tipo, contexto)`.

## 🔭 Visualización 3D de moléculas

Al completar una molécula aparece el botón **«Ver en 3D»**, que abre un modal
responsive con un visor interactivo (rotación con arrastre, zoom con rueda/pellizco).

- Motor: [3Dmol.js](https://3dmol.org) desde CDN (licencia BSD-3-Clause).
- Las coordenadas se calculan en Python (`molecule_3d.py`) con **geometría
  VSEPR básica**: lineal, angular (H₂O 104,5°), piramidal, tetraédrica,
  octaédrica, anillos aromáticos… y un generador genérico de respaldo para
  las orgánicas grandes. El resultado viaja como string **XYZ** incrustado
  en la página.
- Si el CDN no carga (sin internet), el juego sigue funcionando y Octeto avisa.
- API: `GET /api/molecule3d/<mol_id>` devuelve el XYZ en JSON.

## 🧪 Modo Sandbox (`/sandbox`)

Libertad creativa: lienzo donde colocar cualquier átomo de la tabla periódica.

- Los átomos cercanos se **enlazan automáticamente**; también hay herramienta
  «Enlazar» manual y «Borrar átomo». Usable con toques en móvil.
- **Calcular fórmula**: el servidor devuelve la fórmula empírica con el orden
  convencional (NaCl, H₂O, NH₃…) y Octeto la reconoce si es una molécula del juego.
- **Guardar molécula**: la añade a la galería. **Ver en 3D**: convierte tu
  disposición 2D a XYZ y la muestra en el visor.
- Sin validación de valencia: Octeto protesta, pero no impide nada.

## ⚗️ Puzles de reacción (`/reactions`)

Tres reacciones químicas reales para ordenar sus pasos (botones ▲▼, aptos para
móvil) y responder una pregunta clave (catalizador/condición):

1. **Síntesis del agua** (2 H₂ + O₂ → 2 H₂O)
2. **Proceso Haber-Bosch** (N₂ + 3 H₂ → 2 NH₃, catalizador de hierro)
3. **Del vino al vinagre** (oxidación del etanol a ácido acético)

Validación en el servidor (`POST /check_reaction`), puntuación en sesión,
confeti y fanfarria al acertar. Datos y lógica en `reactions.py`.

## 🖼️ Galería (`/gallery`) y 🏅 logros (`/achievements`)

- La sesión de Flask guarda las moléculas completadas en los desafíos y las
  creaciones del sandbox. La galería las muestra con su SVG, curiosidad y
  botón «Ver en 3D».
- **5 logros**: Primera molécula 🧪 · Sin pistas 🧠 · Coleccionista (5) 📦 ·
  Alquimista (10) ⚗️ · Rey del Sandbox (5) 👑. Al desbloquearse, Octeto lo
  anuncia con un toast + confeti. Lógica en `achievements.py`.

## 📖 Misión narrativa (`/story`)

**«El Elixir de la Vida»**: el alquimista Anselmo del Matraz necesita ayuda para
reconstruir su receta, molécula a molécula (de H₂ a etanol). Los diálogos entre
capítulos los narra Octeto. La historia se implementa como un pseudo-nivel
`story` que **reutiliza el motor de juego original** (cero duplicación de
rutas); el progreso se guarda en sesión. Datos en `missions.py`.

## ✨ Mejoras visuales y sonoras

- **Confeti** (canvas-confetti desde CDN, licencia ISC) al completar moléculas,
  reacciones y logros.
- **Sonidos sin archivos**: tonos generados con la **Web Audio API** («pop» al
  colocar, «ding» al acertar, fanfarria al completar, zumbido al fallar).
- La tabla periódica tiene **tooltip** con nombre y valencia al pasar el ratón,
  y los huecos hacen una **animación de encaje** al llenarse.

---

## 📁 Archivos nuevos

```
quimica/
├── octeto.py          ← frases del asistente 🐙
├── ui_common.py       ← widgets compartidos (bocadillo, toasts, sonidos, modal 3D)
├── molecule_3d.py     ← geometrías VSEPR → formato XYZ
├── reactions.py       ← puzles de reacción + validación
├── missions.py        ← misión narrativa "El Elixir de la Vida"
├── achievements.py    ← definición y chequeo de logros
├── views_nuevas.py    ← páginas nuevas (sandbox, reacciones, galería, logros, historia)
├── requirements.txt
└── docs/designs/      ← documento de diseño de esta versión
```

## 🌐 Rutas nuevas

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/sandbox` | GET | Modo libertad creativa |
| `/sandbox/formula` | POST | Fórmula empírica de los átomos colocados |
| `/sandbox/save` | POST | Guardar creación en la galería |
| `/sandbox/xyz` | POST | Convertir el lienzo 2D a XYZ (visor 3D) |
| `/reactions` | GET | Listado de puzles de reacción |
| `/reaction/<id>` | GET | Puzle individual (pasos barajados) |
| `/check_reaction` | POST | Validar orden + pregunta, sumar puntos |
| `/gallery` | GET | Galería de moléculas |
| `/achievements` | GET | Vitrina de logros |
| `/story` | GET | Portada de la misión narrativa |
| `/story/start` | GET | (Re)iniciar la historia |
| `/api/molecule3d/<mol_id>` | GET | XYZ de una molécula en JSON |

## 🚀 Arranque

```bash
pip install -r requirements.txt
python app.py
# http://localhost:5000
```

Las únicas dependencias externas del navegador (3Dmol.js y canvas-confetti)
se cargan desde CDN y son opcionales: sin ellas el juego funciona igual,
solo sin 3D ni confeti.
