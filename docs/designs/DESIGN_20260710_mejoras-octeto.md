# Diseño — Mejoras "Átomos Perdidos" v2 (Octeto, 3D, Sandbox, Reacciones, Galería, Historia)

**Fecha:** 2026-07-10 · **Rama:** `feature/mejoras-octeto`

## Objetivo

Ampliar el juego educativo manteniendo su arquitectura original (Python genera todo
el HTML con f-strings; estado ligero en `session` de Flask) con: asistente con
personalidad (Octeto 🐙), visor 3D de moléculas, modo sandbox, puzles de reacción,
galería + logros, misión narrativa y mejoras visuales/sonoras.

## Arquitectura (módulos nuevos)

| Módulo | Responsabilidad |
|---|---|
| `octeto.py` | Frases de Octeto por evento (`get_octeto_message(tipo, contexto)`) |
| `ui_common.py` | HTML/CSS/JS compartido: bocadillo de Octeto, toasts, sonidos WebAudio, confeti, modal 3D |
| `molecule_3d.py` | Coordenadas 3D aproximadas (VSEPR básica) → formato XYZ para 3Dmol.js. Registro explícito por `svg_key` + fallback genérico |
| `reactions.py` | 3 puzles de reacción (datos + validación pura) |
| `missions.py` | Historia "Elixir de la vida": capítulos → moléculas existentes. Se registra como pseudo-nivel `MOLECULES["story"]` para reutilizar TODO el flujo de juego sin duplicar rutas |
| `achievements.py` | Definición de 5 logros y chequeo contra la sesión |

Rutas nuevas: `/sandbox`, `/sandbox/formula` (POST), `/sandbox/save` (POST),
`/sandbox/xyz` (POST), `/reactions`, `/reaction/<id>`, `/check_reaction` (POST),
`/gallery`, `/achievements`, `/story`, `/api/molecule3d/<mol_id>`.

Las rutas originales **no cambian de contrato**; `render_game_page` se extiende
(widget Octeto, botón 3D, sonidos, confeti, diálogo de historia si `level=="story"`).

## Dependencias frontend (CDN, sin pip nuevos)

- **3Dmol.js** — licencia BSD-3-Clause, proyecto académico mantenido (Koes Lab,
  U. Pittsburgh). Solo se carga en páginas que lo usan (juego/sandbox/galería).
  No envía datos: renderiza localmente el XYZ incrustado.
- **canvas-confetti** — licencia ISC, librería mínima (~10 kB) sin red.
- Sonidos: **Web Audio API** con tonos generados en JS (cero archivos externos).

Si el CDN no carga, el juego sigue funcionando (el botón 3D avisa en vez de romper).

## Persistencia (session Flask)

- `gallery`: lista de dicts mínimos `{tipo, id/nombre, formula, svg_key|atoms}`.
- `achievements`: lista de ids desbloqueados; `pending_toasts` para anunciar.
- `mol_index_story`, `score_story`…: idénticos a los niveles existentes (gratis).
- `reactions_done`, `score_reactions`.
- Cookie de sesión: se guardan solo ids/símbolos, nunca HTML/SVG.

## Riesgos y mitigación

- **Cookie >4 kB** si la galería crece → se guardan datos mínimos y la galería
  se limita a 30 entradas.
- **CDN caído** → detección `typeof $3Dmol === 'undefined'` con mensaje de Octeto.
- **Romper el juego original** → contrato de rutas intacto; prueba manual de
  las rutas viejas y nuevas con el servidor corriendo antes de cerrar.

## Criterios de validación

1. Rutas originales responden 200 y el flujo colocar/pista/siguiente funciona.
2. Cada ruta nueva responde 200 y sus POST devuelven JSON correcto.
3. `molecule_3d.get_xyz()` produce XYZ parseable para las 63 moléculas.
4. `reactions.validar()` acepta el orden correcto y rechaza uno incorrecto.
5. Fórmula empírica: `[H,H,O] → H₂O`, orden Hill con C/H primero.
