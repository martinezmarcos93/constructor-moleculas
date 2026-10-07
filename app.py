"""
app.py  –  Átomos Perdidos: El Constructor de Moléculas
Servidor Flask: toda la lógica y generación de HTML ocurre aquí en Python.
"""

from flask import Flask, session, request, jsonify, redirect
import json, random
from collections import Counter

from config import SECRET_KEY

from periodic_table import ELEMENTS, ELEMENT_POSITIONS, CATEGORY_COLORS, CATEGORY_LABELS
from molecules import GameSession, MOLECULES, LEVEL_LABELS, get_molecule_by_id
from svg_molecules import get_svg

# ── Módulos nuevos (v2) ──
import octeto
import missions
import reactions
import achievements as logros_mod
import views_nuevas
from molecule_3d import get_xyz, xyz_from_sandbox
from svg_molecules import ATOM_COLORS
from chemistry_rules import analyze_formula
from progression import load_progression
from challenge_model import serialize_challenges
from ui_common import (CDN_3DMOL, CDN_CONFETTI, WIDGETS_CSS, SHARED_JS, MOL3D_JS,
                       build_octeto_html, build_mol3d_modal_html,
                       build_pending_toasts_js, build_page)

app = Flask(__name__)
# Clave fija SOLO para desarrollo (la sesión guarda progreso, no datos sensibles)
app.secret_key = SECRET_KEY

# La historia se registra como pseudo-nivel: reutiliza TODO el motor del juego
MOLECULES["story"] = missions.obtener_moleculas_historia()
LEVEL_LABELS["story"] = "📖 Historia"

MAX_GALERIA = 30  # tope de entradas en sesión para no inflar la cookie


# ─────────────────────────────────────────────
# HELPERS DE SESIÓN: galería, logros, fórmula, progresión
# ─────────────────────────────────────────────

def _registrar_progreso(dominio: str, correcto: bool, puntos: int = 1) -> None:
    """Actualiza la maestría pedagógica sin invalidar sesiones antiguas."""
    progression = load_progression(session.get("progression"))
    progression.register(dominio, correcto, puntos)
    session["progression"] = progression.snapshot()
    session.modified = True


def _subindices(n: int) -> str:
    """Convierte 12 → '₁₂' para las fórmulas químicas."""
    subs = "₀₁₂₃₄₅₆₇₈₉"
    return "".join(subs[int(d)] for d in str(n)) if n > 1 else ""


# Secuencia convencional para escribir fórmulas (electropositivo primero):
# da NaCl, H₂O, NH₃, CH₄, H₂SO₄… como se escriben en los libros de texto.
_SECUENCIA_NO_METALES = ["B", "Si", "C", "Sb", "As", "P", "N", "H",
                         "Te", "Se", "S", "At", "I", "Br", "Cl", "O", "F"]
_EN_POR_SIMBOLO = {el["symbol"]: (el["electronegativity"] or 0.0)
                   for el in ELEMENTS.values()}


def calcular_formula(simbolos: list) -> str:
    """
    Fórmula empírica con el orden convencional: metales primero (por
    electronegatividad creciente), luego los no metales en la secuencia
    química estándar (C antes que H, N antes que H, O casi al final…).
    """
    conteo = Counter(s.strip().capitalize() for s in simbolos if s.strip())
    metales = sorted((s for s in conteo if s not in _SECUENCIA_NO_METALES),
                     key=lambda s: (_EN_POR_SIMBOLO.get(s, 0.0), s))
    no_metales = [s for s in _SECUENCIA_NO_METALES if s in conteo]
    return "".join(f"{sym}{_subindices(conteo[sym])}"
                   for sym in metales + no_metales)


def _agregar_a_galeria(entrada: dict):
    """Añade una entrada a la galería en sesión (con tope de tamaño)."""
    galeria = session.get("gallery", [])
    # Los desafíos no se duplican; el sandbox puede repetir fórmula
    if entrada["tipo"] == "desafio" and any(
            g.get("tipo") == "desafio" and g.get("id") == entrada.get("id")
            for g in galeria):
        return
    galeria.append(entrada)
    session["gallery"] = galeria[-MAX_GALERIA:]
    session.modified = True


def _desbloquear_logros(evento: dict) -> list:
    """Comprueba logros, los persiste y devuelve los toasts nuevos."""
    desbloqueados = session.get("achievements", [])
    nuevos = logros_mod.comprobar_logros(desbloqueados, session.get("gallery", []), evento)
    if nuevos:
        session["achievements"] = desbloqueados + nuevos
        session["pending_toasts"] = session.get("pending_toasts", []) + [
            logros_mod.texto_toast(l) for l in nuevos]
        session.modified = True
    return [logros_mod.texto_toast(l) for l in nuevos]


def _sacar_toasts_pendientes() -> list:
    """Extrae (y limpia) los toasts pendientes de la sesión."""
    toasts = session.pop("pending_toasts", [])
    if toasts:
        session.modified = True
    return toasts

# ─────────────────────────────────────────────
# GENERADOR DE HTML  (Python genera todo el HTML)
# ─────────────────────────────────────────────

# CSS extra de la página de juego (v2): tooltip de la tabla, animación de
# encaje, diálogo de historia y botón 3D. Va en string aparte para no pelear
# con las llaves del f-string de la plantilla.
EXTRA_GAME_CSS = """
/* Tooltip de elemento: nombre + valencia */
.element::after{content:attr(data-name) " · valencia " attr(data-valence);position:absolute;
bottom:105%;left:50%;transform:translateX(-50%);background:#0a0a1a;border:1px solid var(--accent);
color:var(--text);padding:3px 8px;border-radius:6px;font-size:9px;white-space:nowrap;opacity:0;
pointer-events:none;transition:opacity .15s;z-index:30}
.element:hover::after{opacity:1}
.element.empty::after{display:none}
/* Animación de "encaje" cuando un hueco se llena */
.atom-slot.filled{animation:encaje .4s cubic-bezier(.3,1.6,.5,1)}
@keyframes encaje{0%{transform:scale(1.45);box-shadow:0 0 0 10px rgba(79,209,197,.35)}
60%{transform:scale(.9)}100%{transform:scale(1);box-shadow:none}}
/* Diálogo de la misión narrativa */
.story-dialog{background:#241a10;border:1px solid #6a4a1a;border-radius:12px;padding:14px 16px;
margin-bottom:14px;font-size:.85rem;line-height:1.6;color:#e8d8b8}
.story-dialog-title{color:var(--warn);font-weight:bold;font-size:.75rem;text-transform:uppercase;
letter-spacing:2px;margin-bottom:8px}
/* Botón Ver en 3D */
.btn-3d{padding:10px 22px;background:linear-gradient(135deg,#2a3a5a,#1a2a4a);border:1px solid #3a5a8a;
border-radius:10px;color:#a8c8f8;font-weight:bold;cursor:pointer;font-family:monospace;font-size:.9rem;
transition:all .2s}
.btn-3d:hover{transform:translateY(-2px);box-shadow:0 4px 16px rgba(58,90,138,.5)}
/* Enlaces de navegación del header */
.header-nav{display:flex;gap:6px;flex-wrap:wrap}
.header-nav a{color:var(--muted);text-decoration:none;font-size:.7rem;padding:4px 8px;
border:1px solid var(--border);border-radius:6px}
.header-nav a:hover{color:var(--accent2);border-color:var(--accent2)}
"""

def build_periodic_table_html():
    """Genera el HTML de la tabla periódica completa desde Python."""
    # Crear grilla 10×18
    grid = {}
    for z, pos in ELEMENT_POSITIONS.items():
        grid[pos] = z

    rows_html = []
    for row in range(1, 11):
        row_html = f'<div class="pt-row" data-row="{row}">'
        for col in range(1, 19):
            z = grid.get((row, col))
            if z:
                el = ELEMENTS[z]
                cat = el["category"]
                color = CATEGORY_COLORS.get(cat, "#999")
                en = el["electronegativity"]
                en_str = f"{en:.2f}" if en else "—"
                row_html += (
                    f'<div class="element" '
                    f'data-z="{z}" data-symbol="{el["symbol"]}" '
                    f'data-name="{el["name"]}" data-cat="{cat}" '
                    f'data-config="{el["config"]}" data-valence="{el["valence"]}" '
                    f'data-en="{en_str}" data-mass="{el["mass"]}" '
                    f'data-period="{el["period"]}" data-group="{el["group"]}" '
                    f'style="background:{color}20; border-color:{color}60" '
                    f'onclick="selectElement(this)" '
                    f'title="{el["name"]} — {el["config"]}">'
                    f'<span class="el-num">{z}</span>'
                    f'<span class="el-sym">{el["symbol"]}</span>'
                    f'<span class="el-name">{el["name"][:8]}</span>'
                    f'<span class="el-mass">{el["mass"]:.1f}</span>'
                    f'</div>'
                )
            elif row in (1, 2, 3, 4, 5, 6, 7):
                # hueco vacío (posición sin elemento en la tabla)
                row_html += '<div class="element empty"></div>'
            else:
                row_html += '<div class="element empty"></div>'
        # Etiqueta de fila lantánidos/actínidos
        if row == 8:
            row_html += '<div class="pt-sep">— Lantánidos / Actínidos —</div>'
        row_html += '</div>'
        rows_html.append(row_html)

    return "\n".join(rows_html)


def build_legend_html():
    html = '<div class="legend">'
    for cat, color in CATEGORY_COLORS.items():
        label = CATEGORY_LABELS.get(cat, cat)
        html += (f'<span class="legend-item" style="background:{color}40;border-color:{color}">'
                 f'{label}</span>')
    html += '</div>'
    return html


def render_game_page(level: str, mol_index: int, score: int,
                     hints_used: int, filled: dict,
                     feedback: str = "", completed: bool = False):
    """Genera la página completa del juego. Python controla todo."""

    mols = MOLECULES.get(level, [])
    if mol_index >= len(mols):
        return render_finished_page(level, score)

    mol = mols[mol_index]
    total = len(mols)
    hints_remaining = 3 - hints_used

    # Barra de progreso
    progress_pct = int(mol_index / total * 100)

    # Construir los átomos de la molécula
    atoms_html = '<div class="molecule-display">'
    for i, sym in enumerate(mol["atoms"]):
        if i in mol["missing"]:
            filled_sym = filled.get(str(i), "")
            if filled_sym:
                atoms_html += (
                    f'<div class="atom-slot filled" data-slot="{i}" onclick="clearSlot({i})">'
                    f'<span class="slot-sym">{filled_sym}</span>'
                    f'<span class="slot-hint">✕</span>'
                    f'</div>'
                )
            else:
                atoms_html += (
                    f'<div class="atom-slot empty-slot" data-slot="{i}" onclick="clickSlot({i})">'
                    f'<span>?</span>'
                    f'</div>'
                )
        else:
            atoms_html += f'<div class="atom-slot known"><span>{sym}</span></div>'
        # Separador entre átomos
        if i < len(mol["atoms"]) - 1:
            atoms_html += '<div class="bond-line"></div>'
    atoms_html += '</div>'

    # Pistas ya usadas
    hints_list_html = ""
    hint_session_key = f"hints_{level}_{mol_index}"
    used_hints = session.get(hint_session_key, [])
    if used_hints:
        hints_list_html = "<ul class='hints-used'>"
        for idx, h in enumerate(used_hints):
            hints_list_html += f"<li>💡 Pista {idx+1}: {h}</li>"
        hints_list_html += "</ul>"

    # ── Mensaje contextual de Octeto 🐙 ──
    if completed:
        octeto_msg = octeto.get_octeto_message("molecula_completa")
    elif feedback and "Incorrecto" in feedback:
        octeto_msg = octeto.get_octeto_message("elemento_incorrecto")
    elif used_hints:
        octeto_msg = octeto.get_octeto_message(
            "pista_usada", {"numero": len(used_hints), "pista": used_hints[-1]})
    elif filled:
        octeto_msg = octeto.get_octeto_message("elemento_colocado")
    else:
        octeto_msg = octeto.get_octeto_message("bienvenida")

    # ── Diálogo de la historia (solo en el pseudo-nivel "story") ──
    story_html = ""
    if level == "story":
        dialogo = missions.obtener_dialogo(mol_index)
        if dialogo:
            story_html = (
                '<div class="story-dialog">'
                f'<div class="story-dialog-title">📖 {missions.MISSION["titulo"]} '
                f'— capítulo {mol_index + 1}/{total}</div>'
                f'<p>{dialogo}</p></div>'
            )

    # Botón de pista
    hint_btn = (
        f'<button class="btn-hint" onclick="requestHint()" '
        f'{"disabled" if hints_remaining == 0 else ""}>'
        f'💡 Pedir pista ({hints_remaining} restantes)</button>'
        if not completed else ""
    )

    # SVG de la molécula (solo si completada) + botón para verla en 3D
    svg_section = ""
    mol_xyz = ""
    if completed:
        svg_content = get_svg(mol["svg_key"])
        mol_xyz = get_xyz(mol["svg_key"], mol["atoms"], mol["name"])
        btn_3d = ('<button class="btn-3d" onclick=\'openMol3D(MOL_XYZ, '
                  + json.dumps(f"{mol['name']} ({mol['id']})", ensure_ascii=False)
                  + ')\'>🔭 Ver en 3D</button>') if mol_xyz else ""
        svg_section = f"""
        <div class="completed-section">
            <div class="molecule-svg">{svg_content}</div>
            {btn_3d}
            <div class="fun-fact">
                <h3>🔬 {mol['name']} ({mol['formula']})</h3>
                <p>{mol['fun_fact']}</p>
            </div>
            <button class="btn-next" onclick="nextMolecule()">
                {'🏆 Ver resultados' if mol_index + 1 >= total else '➡️ Siguiente molécula'}
            </button>
        </div>
        """

    # Tabla periódica
    pt_html = build_periodic_table_html()
    legend_html = build_legend_html()

    # Panel de elemento seleccionado
    el_panel = """
    <div class="el-panel" id="el-panel">
        <div class="el-panel-header">
            <span id="ep-symbol">—</span>
            <span id="ep-name">Selecciona un elemento</span>
        </div>
        <div class="el-panel-body">
            <div class="ep-row"><b>Z:</b> <span id="ep-z">—</span></div>
            <div class="ep-row"><b>Masa:</b> <span id="ep-mass">—</span></div>
            <div class="ep-row"><b>Config:</b> <span id="ep-config">—</span></div>
            <div class="ep-row"><b>Valencia:</b> <span id="ep-valence">—</span></div>
            <div class="ep-row"><b>Grupo/Período:</b> <span id="ep-gp">—</span></div>
            <div class="ep-row"><b>Electr.:</b> <span id="ep-en">—</span></div>
            <div class="ep-row"><b>Categoría:</b> <span id="ep-cat">—</span></div>
        </div>
        <button class="btn-place" id="btn-place" onclick="placeElement()" disabled>
            ⚗️ Colocar en hueco
        </button>
    </div>
    """

    # Feedback
    feedback_html = ""
    if feedback:
        is_ok = "ok" in feedback.lower() or "correc" in feedback.lower() or "¡" in feedback
        fc = "feedback-ok" if is_ok else "feedback-err"
        feedback_html = f'<div class="feedback {fc}">{feedback}</div>'

    # Datos para JS (controlados desde Python)
    game_data = json.dumps({
        "level": level,
        "molIndex": mol_index,
        "missingSlots": mol["missing"],
        "filled": filled,
        "completed": completed,
        "score": score,
        "hintsUsed": hints_used,
        "molId": mol["id"],
    })

    # Widgets v2: Octeto, modal 3D y toasts de logros pendientes
    octeto_widget = build_octeto_html(octeto_msg)
    modal_3d_html = build_mol3d_modal_html()
    toasts_js = build_pending_toasts_js(_sacar_toasts_pendientes())

    # ── Plantilla HTML completa ───────────────
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Átomos Perdidos 🔬</title>
{CDN_CONFETTI}
{CDN_3DMOL}
<style>
/* ── Variables y reset ── */
:root {{
  --bg:       #0d0d1a;
  --surface:  #151528;
  --card:     #1e1e38;
  --border:   #2e2e55;
  --accent:   #7c6af7;
  --accent2:  #4fd1c5;
  --text:     #e8e8f0;
  --muted:    #8888aa;
  --success:  #4ade80;
  --error:    #f87171;
  --warn:     #fbbf24;
}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:'Courier New',monospace;min-height:100vh;overflow-x:hidden}}
/* ── Header ── */
.header{{background:linear-gradient(135deg,#1a1a3e,#0d1a2e);border-bottom:1px solid var(--border);padding:12px 20px;display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}}
.logo{{font-size:1.4rem;font-weight:bold;background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.meta{{display:flex;gap:16px;align-items:center;font-size:.85rem;color:var(--muted)}}
.score-badge{{background:var(--accent);color:#fff;padding:4px 12px;border-radius:20px;font-weight:bold}}
.progress-bar{{height:4px;background:var(--border);border-radius:2px;margin-top:6px}}
.progress-fill{{height:4px;background:linear-gradient(90deg,var(--accent),var(--accent2));border-radius:2px;transition:width .4s;width:{progress_pct}%}}
/* ── Layout principal ── */
.main{{display:grid;grid-template-columns:1fr 280px;grid-template-rows:auto 1fr;gap:12px;padding:12px;max-width:1600px;margin:0 auto}}
/* ── Molécula ── */
.mol-section{{grid-column:1/-1;background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px}}
.mol-title{{font-size:.8rem;color:var(--muted);text-transform:uppercase;letter-spacing:2px;margin-bottom:8px}}
.mol-formula{{font-size:1.5rem;color:var(--accent2);margin-bottom:16px;font-weight:bold}}
.molecule-display{{display:flex;align-items:center;flex-wrap:wrap;gap:6px;min-height:70px}}
.atom-slot{{width:58px;height:58px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:bold;font-size:1.1rem;cursor:pointer;transition:all .2s;border:2px solid var(--border);position:relative}}
.atom-slot.known{{background:#1a2a1a;color:var(--accent2);border-color:#2a4a2a;cursor:default}}
.atom-slot.empty-slot{{background:#2a1a3a;color:var(--warn);border-color:var(--accent);border-style:dashed;animation:pulse 2s infinite}}
.atom-slot.empty-slot:hover{{background:#3a2a4a;transform:scale(1.08)}}
.atom-slot.filled{{background:#1a3a2a;color:var(--success);border-color:var(--success)}}
.atom-slot.filled .slot-hint{{font-size:.55rem;color:var(--muted);display:block}}
.bond-line{{width:22px;height:3px;background:var(--muted);border-radius:2px;flex-shrink:0}}
@keyframes pulse{{0%,100%{{box-shadow:0 0 0 0 rgba(124,106,247,.4)}}50%{{box-shadow:0 0 0 8px rgba(124,106,247,0)}}}}
/* ── Tabla periódica ── */
.pt-section{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:12px;overflow-x:auto}}
.pt-row{{display:flex;gap:2px;margin-bottom:2px}}
.element{{width:44px;height:52px;border:1px solid transparent;border-radius:4px;padding:2px;cursor:pointer;transition:all .15s;display:flex;flex-direction:column;align-items:center;justify-content:space-between;font-family:monospace;flex-shrink:0;position:relative}}
.element:hover{{transform:scale(1.15);z-index:10;border-color:#fff !important}}
.element.selected{{outline:2px solid var(--accent2);outline-offset:1px;transform:scale(1.1);z-index:5}}
.element.empty{{background:transparent!important;border-color:transparent!important;cursor:default;pointer-events:none}}
.el-num{{font-size:7px;color:var(--muted);align-self:flex-start;line-height:1}}
.el-sym{{font-size:13px;font-weight:bold;color:var(--text);line-height:1}}
.el-name{{font-size:6px;color:var(--muted);text-align:center;overflow:hidden;max-width:42px;white-space:nowrap}}
.el-mass{{font-size:6px;color:var(--muted)}}
.pt-sep{{width:100%;text-align:center;color:var(--muted);font-size:.7rem;padding:4px 0;letter-spacing:2px}}
.legend{{display:flex;flex-wrap:wrap;gap:4px;margin-top:8px}}
.legend-item{{font-size:.65rem;padding:2px 6px;border-radius:10px;border:1px solid;color:var(--text)}}
/* ── Panel lateral ── */
.side-panel{{display:flex;flex-direction:column;gap:10px}}
.el-panel{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px}}
.el-panel-header{{display:flex;align-items:baseline;gap:10px;margin-bottom:12px;border-bottom:1px solid var(--border);padding-bottom:10px}}
#ep-symbol{{font-size:2rem;font-weight:bold;color:var(--accent2);min-width:40px}}
#ep-name{{font-size:.9rem;color:var(--muted)}}
.ep-row{{display:flex;gap:8px;font-size:.8rem;padding:3px 0;border-bottom:1px solid #1a1a2e}}
.ep-row b{{color:var(--muted);min-width:70px}}
.btn-place{{width:100%;margin-top:12px;padding:10px;background:linear-gradient(135deg,var(--accent),#5a4ad7);border:none;border-radius:8px;color:#fff;font-weight:bold;cursor:pointer;transition:all .2s;font-family:monospace;font-size:.9rem}}
.btn-place:hover:not(:disabled){{transform:translateY(-1px);box-shadow:0 4px 15px rgba(124,106,247,.4)}}
.btn-place:disabled{{opacity:.4;cursor:not-allowed}}
/* ── Pistas ── */
.hints-section{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px}}
.hints-section h3{{font-size:.8rem;color:var(--muted);text-transform:uppercase;letter-spacing:2px;margin-bottom:10px}}
.btn-hint{{width:100%;padding:10px;background:linear-gradient(135deg,#2a3a1a,#1a2a0a);border:1px solid #4a6a2a;border-radius:8px;color:var(--warn);cursor:pointer;transition:all .2s;font-family:monospace;font-size:.85rem;margin-bottom:10px}}
.btn-hint:hover:not(:disabled){{background:linear-gradient(135deg,#3a4a2a,#2a3a1a)}}
.btn-hint:disabled{{opacity:.4;cursor:not-allowed}}
.hints-used{{list-style:none;display:flex;flex-direction:column;gap:6px}}
.hints-used li{{background:#1a2a0a;border:1px solid #2a4a1a;border-radius:6px;padding:8px;font-size:.75rem;color:#a8d8a8;line-height:1.4}}
/* ── Feedback ── */
.feedback{{padding:10px 14px;border-radius:8px;font-size:.85rem;font-weight:bold;border:1px solid}}
.feedback-ok{{background:#0a2a0a;border-color:var(--success);color:var(--success)}}
.feedback-err{{background:#2a0a0a;border-color:var(--error);color:var(--error)}}
/* ── Sección completada ── */
.completed-section{{margin-top:20px;border-top:1px solid var(--border);padding-top:20px;display:flex;flex-direction:column;gap:16px;align-items:center}}
.molecule-svg{{background:#0d0d1a;border-radius:12px;padding:16px;border:1px solid var(--border)}}
.fun-fact{{background:#0a1a2a;border:1px solid #1a3a5a;border-radius:10px;padding:16px;max-width:500px}}
.fun-fact h3{{color:var(--accent2);margin-bottom:8px;font-size:1rem}}
.fun-fact p{{color:var(--muted);font-size:.85rem;line-height:1.6}}
.btn-next{{padding:12px 28px;background:linear-gradient(135deg,var(--accent2),#38b2ac);border:none;border-radius:10px;color:#000;font-weight:bold;font-size:1rem;cursor:pointer;transition:all .2s;font-family:monospace}}
.btn-next:hover{{transform:translateY(-2px);box-shadow:0 6px 20px rgba(79,209,197,.4)}}
/* ── Responsive ── */
@media(max-width:900px){{
  .main{{grid-template-columns:1fr}}
  .element{{width:34px;height:42px}}
  .el-sym{{font-size:10px}}
  .el-num,.el-name,.el-mass{{font-size:5px}}
}}
/* ── Scrollbar ── */
::-webkit-scrollbar{{width:6px;height:6px}}
::-webkit-scrollbar-track{{background:var(--bg)}}
::-webkit-scrollbar-thumb{{background:var(--border);border-radius:3px}}
{EXTRA_GAME_CSS}
{WIDGETS_CSS}
</style>
</head>
<body>

<div class="header">
  <div>
    <div class="logo">⚗️ Átomos Perdidos</div>
    <div class="progress-bar"><div class="progress-fill"></div></div>
  </div>
  <div class="meta">
    <span>Nivel: <b style="color:var(--accent)">{LEVEL_LABELS.get(level,'')}</b></span>
    <span>Molécula: <b>{mol_index+1}/{total}</b></span>
    <span class="score-badge">🏆 {score} pts</span>
    <div class="header-nav">
      <a href="/">🏠 Inicio</a>
      <a href="/sandbox">🧪 Sandbox</a>
      <a href="/reactions">⚗️ Reacciones</a>
      <a href="/gallery">🖼️ Galería</a>
    </div>
  </div>
</div>

<div class="main">
  <!-- Molécula incompleta -->
  <div class="mol-section">
    {story_html}
    <div class="mol-title">Completa la molécula</div>
    <div class="mol-formula">{mol['formula']}</div>
    {atoms_html}
    {feedback_html}
    {svg_section}
  </div>

  <!-- Tabla periódica -->
  <div class="pt-section">
    <div style="font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:2px;margin-bottom:8px">Tabla Periódica</div>
    {pt_html}
    {legend_html}
  </div>

  <!-- Panel lateral -->
  <div class="side-panel">
    {el_panel}
    <div class="hints-section">
      <h3>💡 Sistema de Pistas</h3>
      {hint_btn}
      {hints_list_html}
    </div>
  </div>
</div>

{octeto_widget}
{modal_3d_html}

<script>
{SHARED_JS}
{MOL3D_JS}
{toasts_js}

// ── Estado del juego (generado por Python, consumido por JS) ──
const GAME = {game_data};
const MOL_XYZ = {json.dumps(mol_xyz)};

let selectedElement = null;
let activeSlot = null;

// ── Selección de elemento en la tabla ──
function selectElement(el) {{
  document.querySelectorAll('.element.selected').forEach(e => e.classList.remove('selected'));
  el.classList.add('selected');
  selectedElement = {{
    symbol:  el.dataset.symbol,
    name:    el.dataset.name,
    z:       el.dataset.z,
    mass:    el.dataset.mass,
    config:  el.dataset.config,
    valence: el.dataset.valence,
    en:      el.dataset.en,
    period:  el.dataset.period,
    group:   el.dataset.group,
    cat:     el.dataset.cat,
  }};
  document.getElementById('ep-symbol').textContent = selectedElement.symbol;
  document.getElementById('ep-name').textContent   = selectedElement.name;
  document.getElementById('ep-z').textContent      = selectedElement.z;
  document.getElementById('ep-mass').textContent   = selectedElement.mass + ' u';
  document.getElementById('ep-config').textContent = selectedElement.config;
  document.getElementById('ep-valence').textContent= selectedElement.valence;
  document.getElementById('ep-gp').textContent     = `G${{selectedElement.group}} / P${{selectedElement.period}}`;
  document.getElementById('ep-en').textContent     = selectedElement.en;
  const catMap = {json.dumps(CATEGORY_LABELS)};
  document.getElementById('ep-cat').textContent    = catMap[selectedElement.cat] || selectedElement.cat;
  document.getElementById('btn-place').disabled = (activeSlot === null);
}}

// ── Click en un hueco ──
function clickSlot(slotIdx) {{
  activeSlot = slotIdx;
  document.querySelectorAll('.atom-slot.empty-slot').forEach(s => s.style.borderColor = '');
  const target = document.querySelector(`.atom-slot[data-slot="${{slotIdx}}"]`);
  if (target) target.style.borderColor = '#4fd1c5';
  if (selectedElement) document.getElementById('btn-place').disabled = false;
}}

// ── Limpiar un hueco lleno ──
function clearSlot(slotIdx) {{
  if (GAME.completed) return;
  fetch('/clear_slot', {{
    method: 'POST',
    headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{slot: slotIdx, level: GAME.level, mol_index: GAME.molIndex}})
  }}).then(() => location.reload());
}}

// ── Colocar elemento en hueco ──
function placeElement() {{
  if (!selectedElement || activeSlot === null) return;
  playPop();   // sonidito de colocación (Web Audio, sin archivos)
  fetch('/place_element', {{
    method: 'POST',
    headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{
      slot:      activeSlot,
      symbol:    selectedElement.symbol,
      level:     GAME.level,
      mol_index: GAME.molIndex,
    }})
  }})
  .then(r => r.json())
  .then(data => {{
    if (data.reload) location.reload();
  }});
}}

// ── Pedir pista ──
function requestHint() {{
  fetch('/hint', {{
    method: 'POST',
    headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{level: GAME.level, mol_index: GAME.molIndex}})
  }}).then(() => location.reload());
}}

// ── Siguiente molécula ──
function nextMolecule() {{
  fetch('/next_molecule', {{
    method: 'POST',
    headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{level: GAME.level}})
  }}).then(() => location.reload());
}}

// Highlight si ya hay un slot activo
document.addEventListener('DOMContentLoaded', () => {{
  const missing = GAME.missingSlots;
  const filled  = GAME.filled;
  // Si solo hay un hueco y no está lleno, activarlo automáticamente
  const empty = missing.filter(i => !filled[String(i)]);
  if (empty.length === 1) {{
    activeSlot = empty[0];
    if (selectedElement) document.getElementById('btn-place').disabled = false;
  }}
  // Celebración al cargar la página con la molécula recién completada
  if (GAME.completed) {{
    fireConfetti();
    try {{ playFanfare(); }} catch(e) {{}}
  }}
}});
</script>
</body>
</html>"""
    return html


HOME_CSS = """
.hero{text-align:center;margin:30px 0 34px}
.title{font-size:3rem;font-weight:bold;background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.2}
.subtitle{color:var(--muted);font-size:1rem;margin:10px auto 0;max-width:520px}
.levels{display:flex;gap:20px;flex-wrap:wrap;justify-content:center}
.level-card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:26px 34px;text-align:center;cursor:pointer;transition:all .3s;text-decoration:none;color:var(--text);min-width:190px}
.level-card:hover{transform:translateY(-6px);border-color:var(--accent);box-shadow:0 8px 30px rgba(124,106,247,.25)}
.level-icon{font-size:2.6rem;margin-bottom:10px}
.level-name{font-size:1.3rem;font-weight:bold;margin-bottom:8px}
.level-desc{font-size:.78rem;color:var(--muted);line-height:1.5}
.easy-card .level-name{color:#4ade80}
.medium-card .level-name{color:#fbbf24}
.hard-card .level-name{color:#f87171}
.modes-title{text-align:center;color:var(--muted);font-size:.8rem;text-transform:uppercase;letter-spacing:3px;margin:36px 0 16px}
.modes{display:flex;gap:14px;flex-wrap:wrap;justify-content:center}
.mode-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:18px 24px;text-align:center;text-decoration:none;color:var(--text);min-width:160px;transition:all .25s}
.mode-card:hover{transform:translateY(-4px);border-color:var(--accent2)}
.mode-icon{font-size:2rem;margin-bottom:8px}
.mode-name{font-weight:bold;font-size:.95rem;margin-bottom:5px;color:var(--accent2)}
.mode-desc{font-size:.7rem;color:var(--muted);line-height:1.4}
.footer{margin:40px 0 60px;color:var(--muted);font-size:.75rem;text-align:center}
.atoms-bg{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;overflow:hidden;z-index:-1}
.float-atom{position:absolute;border-radius:50%;opacity:.06;animation:float linear infinite}
@keyframes float{0%{transform:translateY(100vh) rotate(0deg)}100%{transform:translateY(-200px) rotate(360deg)}}
"""


def render_home():
    """Página de inicio: niveles clásicos + los modos nuevos."""
    body = """
<div class="atoms-bg">
  <div class="float-atom" style="width:60px;height:60px;background:#7c6af7;left:10%;animation-duration:15s;animation-delay:0s"></div>
  <div class="float-atom" style="width:40px;height:40px;background:#4fd1c5;left:30%;animation-duration:20s;animation-delay:3s"></div>
  <div class="float-atom" style="width:80px;height:80px;background:#f87171;left:60%;animation-duration:18s;animation-delay:6s"></div>
  <div class="float-atom" style="width:50px;height:50px;background:#fbbf24;left:80%;animation-duration:12s;animation-delay:1s"></div>
</div>
<div class="hero">
  <div class="title">⚗️ Átomos Perdidos</div>
  <div style="font-size:1.2rem;color:#7c6af7;margin:8px 0">El Constructor de Moléculas</div>
  <p class="subtitle">Completa moléculas usando la tabla periódica interactiva. Usa pistas basadas en configuración electrónica para descubrir los átomos que faltan.</p>
</div>
<div class="levels">
  <a href="/game/easy" class="level-card easy-card">
    <div class="level-icon">🟢</div>
    <div class="level-name">Fácil</div>
    <div class="level-desc">Moléculas diatómicas<br>H₂, O₂, HCl, NaCl...<br>Falta 1 átomo</div>
  </a>
  <a href="/game/medium" class="level-card medium-card">
    <div class="level-icon">🟡</div>
    <div class="level-name">Medio</div>
    <div class="level-desc">H₂O, CO₂, NH₃, CH₄...<br>Faltan 1–2 átomos</div>
  </a>
  <a href="/game/hard" class="level-card hard-card">
    <div class="level-icon">🔴</div>
    <div class="level-name">Difícil</div>
    <div class="level-desc">H₂SO₄, C₂H₅OH, CaCO₃...<br>Faltan 2–3 átomos</div>
  </a>
</div>

<div class="modes-title">— Nuevos modos de juego —</div>
<div class="modes">
  <a href="/sandbox" class="mode-card">
    <div class="mode-icon">🧪</div>
    <div class="mode-name">Sandbox</div>
    <div class="mode-desc">Construye cualquier molécula<br>sin reglas ni límites</div>
  </a>
  <a href="/reactions" class="mode-card">
    <div class="mode-icon">⚗️</div>
    <div class="mode-name">Reacciones</div>
    <div class="mode-desc">Ordena los pasos de<br>reacciones químicas reales</div>
  </a>
  <a href="/story" class="mode-card">
    <div class="mode-icon">📖</div>
    <div class="mode-name">Historia</div>
    <div class="mode-desc">Ayuda al alquimista a<br>crear el Elixir de la Vida</div>
  </a>
  <a href="/gallery" class="mode-card">
    <div class="mode-icon">🖼️</div>
    <div class="mode-name">Galería</div>
    <div class="mode-desc">Tu colección de<br>moléculas completadas</div>
  </a>
  <a href="/achievements" class="mode-card">
    <div class="mode-icon">🏅</div>
    <div class="mode-name">Logros</div>
    <div class="mode-desc">Tus medallas de<br>química de campeonato</div>
  </a>
</div>

<div class="footer">
  <p>118 elementos · Configuraciones electrónicas completas · 63 moléculas</p>
  <p style="margin-top:4px">Motor: Python + Flask · Todo el HTML generado dinámicamente desde Python</p>
</div>
"""
    return build_page(
        title="Átomos Perdidos 🔬",
        body=body, active_nav="/",
        octeto_msg=octeto.get_octeto_message("bienvenida"),
        extra_css=HOME_CSS,
        pending_toasts=_sacar_toasts_pendientes(),
    )


FINISHED_CSS = """
.fin-card{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:40px;
text-align:center;max-width:540px;width:100%;margin:40px auto}
.big-stars{font-size:3rem;margin-bottom:16px}
.fin-card h1{font-size:2rem;background:linear-gradient(135deg,var(--accent),var(--accent2));
-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
.fin-score{font-size:3rem;font-weight:bold;color:var(--accent2);margin:20px 0}
.fin-sub{color:var(--muted);font-size:.9rem;margin-bottom:28px}
.fin-btns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.fin-final{background:#1a2a0a;border:1px solid #2a4a1a;border-radius:12px;padding:16px;
color:#c8e8a8;font-size:.85rem;line-height:1.6;text-align:left;margin-bottom:22px}
"""


def render_finished_page(level: str, score: int):
    total = len(MOLECULES.get(level, []))
    max_score = total * 10
    pct = int(score / max_score * 100) if max_score else 0
    stars = "⭐" * (1 + (pct >= 50) + (pct >= 80) + (pct >= 100))

    # Epílogo si es el final de la misión narrativa
    final_html = ""
    titulo = "¡Nivel completado!"
    if level == "story":
        titulo = "¡Misión cumplida!"
        final_html = f'<div class="fin-final">{missions.MISSION["final"]}</div>'

    body = f"""
<div class="fin-card">
  <div class="big-stars">{stars}</div>
  <h1>{titulo}</h1>
  <div class="fin-score">{score} pts</div>
  <div class="fin-sub">Nivel {LEVEL_LABELS.get(level,'')} — {total} moléculas — Máximo posible: {max_score} pts<br>Puntuación: {pct}%</div>
  {final_html}
  <div class="fin-btns">
    <a href="/game/{level}" class="btn btn-primary">🔁 Repetir nivel</a>
    <a href="/gallery" class="btn btn-teal">🖼️ Ver galería</a>
    <a href="/" class="btn btn-ghost">🏠 Inicio</a>
  </div>
</div>
"""
    return build_page(
        title="¡Completado! — Átomos Perdidos",
        body=body, octeto_msg=octeto.get_octeto_message("nivel_completado"),
        extra_css=FINISHED_CSS,
        extra_js="document.addEventListener('DOMContentLoaded',()=>{fireConfetti();try{playFanfare()}catch(e){}});",
        pending_toasts=_sacar_toasts_pendientes(),
    )


# ─────────────────────────────────────────────
# RUTAS FLASK
# ─────────────────────────────────────────────

@app.route("/")
def index():
    return render_home()


@app.route("/game/<level>")
def game(level):
    if level not in MOLECULES:
        return "Nivel no válido", 404
    # Resetear estado del nivel
    session[f"mol_index_{level}"] = 0
    session[f"score_{level}"]     = 0
    session[f"hints_{level}_0"]   = []
    session[f"filled_{level}_0"]  = {}
    return redirect(f"/game/{level}/play")


@app.route("/place_element", methods=["POST"])
def place_element():
    data      = request.get_json()
    level     = data["level"]
    mol_index = int(data["mol_index"])
    slot      = int(data["slot"])
    symbol    = data["symbol"]

    mol       = MOLECULES[level][mol_index]
    expected  = mol["atoms"][slot]

    filled_key  = f"filled_{level}_{mol_index}"
    hints_key   = f"hints_{level}_{mol_index}"
    score_key   = f"score_{level}"
    filled      = session.get(filled_key, {})
    hints_used  = len(session.get(hints_key, []))

    correct = symbol.strip().capitalize() == expected

    if correct:
        filled[str(slot)] = symbol
        session[filled_key] = filled
        session.modified = True

        # ¿Todos los huecos llenos?
        all_filled = all(
            filled.get(str(i), "") == mol["atoms"][i]
            for i in mol["missing"]
        )
        if all_filled:
            points = max(10 - hints_used * 3, 1)
            session[score_key] = session.get(score_key, 0) + points
            _registrar_progreso("moleculas", True, min(points, 5))
            session.modified = True
            # v2: registrar en la galería y comprobar logros
            _agregar_a_galeria({"tipo": "desafio", "id": mol["id"]})
            _desbloquear_logros({"molecula_completada": True,
                                 "hints_usados": hints_used})
            return jsonify({"reload": True, "completed": True})
        return jsonify({"reload": True})
    else:
        _registrar_progreso("moleculas", False, 1)
        return jsonify({"reload": True, "error": f"Incorrecto. '{symbol}' no es el átomo esperado."})


@app.route("/clear_slot", methods=["POST"])
def clear_slot():
    data      = request.get_json()
    level     = data["level"]
    mol_index = int(data["mol_index"])
    slot      = int(data["slot"])
    filled_key = f"filled_{level}_{mol_index}"
    filled = session.get(filled_key, {})
    filled.pop(str(slot), None)
    session[filled_key] = filled
    session.modified = True
    return jsonify({"ok": True})


@app.route("/hint", methods=["POST"])
def hint():
    data      = request.get_json()
    level     = data["level"]
    mol_index = int(data["mol_index"])
    mol       = MOLECULES[level][mol_index]
    hints_key = f"hints_{level}_{mol_index}"
    used      = session.get(hints_key, [])
    if len(used) < 3:
        used.append(mol["hints"][len(used)])
        session[hints_key] = used
        session.modified = True
    return jsonify({"ok": True})


@app.route("/next_molecule", methods=["POST"])
def next_molecule():
    data  = request.get_json()
    level = data["level"]
    idx_key = f"mol_index_{level}"
    session[idx_key] = session.get(idx_key, 0) + 1
    session.modified = True
    return jsonify({"ok": True})


@app.route("/current_game")
def current_game():
    """Devuelve el estado actual — útil para debug."""
    level = request.args.get("level", "easy")
    mol_index = session.get(f"mol_index_{level}", 0)
    score     = session.get(f"score_{level}", 0)
    filled    = session.get(f"filled_{level}_{mol_index}", {})
    hints     = session.get(f"hints_{level}_{mol_index}", [])
    return render_game_page(
        level=level,
        mol_index=mol_index,
        score=score,
        hints_used=len(hints),
        filled=filled,
    )


@app.route("/api/elements")
def api_elements():
    """API JSON: todos los elementos (para tests/extensiones)."""
    return jsonify(ELEMENTS)


@app.route("/api/molecules")
def api_molecules():
    """API JSON: todas las moléculas."""
    return jsonify(MOLECULES)


@app.route("/api/progression")
def api_progression():
    """Estado de maestría del jugador para futuras interfaces adaptativas."""
    return jsonify(load_progression(session.get("progression")).snapshot())


@app.route("/api/challenges")
def api_challenges():
    """Catálogo pedagógico generado a partir de las moléculas existentes."""
    return jsonify(serialize_challenges(MOLECULES))


# ─────────────────────────────────────────────
# Para render_game_page con estado de sesión completo
# ─────────────────────────────────────────────
@app.route("/game/<level>/play")
def play(level):
    if level not in MOLECULES:
        return "Nivel no válido", 404
    mol_index = session.get(f"mol_index_{level}", 0)
    score     = session.get(f"score_{level}", 0)
    filled    = session.get(f"filled_{level}_{mol_index}", {})
    hints     = session.get(f"hints_{level}_{mol_index}", [])

    mols = MOLECULES[level]
    if mol_index >= len(mols):
        return render_finished_page(level, score)

    mol = mols[mol_index]
    # ¿Completada?
    all_filled = all(
        filled.get(str(i), "") == mol["atoms"][i]
        for i in mol["missing"]
    )

    return render_game_page(
        level=level,
        mol_index=mol_index,
        score=score,
        hints_used=len(hints),
        filled=filled,
        completed=all_filled,
    )





# ─────────────────────────────────────────────
# RUTAS NUEVAS v2: SANDBOX
# ─────────────────────────────────────────────

@app.route("/sandbox")
def sandbox():
    """Modo libertad creativa: construir cualquier molécula."""
    return views_nuevas.render_sandbox_page(
        octeto_msg=octeto.get_octeto_message("sandbox_libertad"),
        frases_valencia=[octeto.get_octeto_message("sandbox_sin_valencia")
                         for _ in range(2)],
        colores_atomos=ATOM_COLORS,
    )


@app.route("/sandbox/formula", methods=["POST"])
def sandbox_formula():
    """Calcula la fórmula empírica de los átomos colocados en el lienzo."""
    data = request.get_json() or {}
    simbolos = data.get("simbolos", [])
    if not simbolos:
        return jsonify({"formula": "", "mensaje": "🐙 No hay átomos que contar."})
    known_formulas = {
        m["formula"] for level_mols in MOLECULES.values()
        for m in level_mols
    }
    analysis = analyze_formula(simbolos, known_formulas)
    formula = analysis.formula

    conocida = next(
        (
            m for level_mols in MOLECULES.values()
            for m in level_mols
            if m["formula"] == formula
        ),
        None,
    )
    if conocida:
        mensaje = (
            f"🐙 ¡Eso es {conocida['name']} ({conocida['formula']})! "
            f"La reconocería con los ocho ojos cerrados."
        )
    elif not analysis.plausible:
        mensaje = f"🐙 {analysis.message} La fórmula calculada es {formula}."
    else:
        mensaje = (
            f"🐙 Fórmula calculada: {formula}. "
            f"{analysis.message}"
        )
    return jsonify({
        "formula": formula,
        "mensaje": mensaje,
        "known": analysis.known,
        "plausible": analysis.plausible,
        "elements": analysis.elements,
    })


@app.route("/sandbox/save", methods=["POST"])
def sandbox_save():
    """Guarda la creación del sandbox en la galería (sesión)."""
    data = request.get_json() or {}
    atoms = data.get("atoms", [])[:40]   # tope: la cookie de sesión es finita
    if not atoms:
        return jsonify({"ok": False, "mensaje": "🐙 Nada que guardar."})
    formula = calcular_formula([a["s"] for a in atoms])
    _agregar_a_galeria({"tipo": "sandbox", "formula": formula, "atoms": atoms})
    toasts = _desbloquear_logros({})
    return jsonify({"ok": True, "formula": formula, "toasts": toasts,
                    "mensaje": f"🐙 ¡{formula} guardada en la galería! Mi vitrina y yo estamos orgullosos."})


@app.route("/sandbox/xyz", methods=["POST"])
def sandbox_xyz():
    """Convierte los átomos del lienzo 2D a XYZ para el visor 3D."""
    data = request.get_json() or {}
    atoms = [{"sym": a["s"], "x": a["x"], "y": a["y"]}
             for a in data.get("atoms", [])[:60]]
    return jsonify({"xyz": xyz_from_sandbox(atoms)})


# ─────────────────────────────────────────────
# RUTAS NUEVAS v2: PUZLES DE REACCIÓN
# ─────────────────────────────────────────────

@app.route("/reactions")
def reactions_list():
    """Listado de puzles de reacción."""
    return views_nuevas.render_reactions_page(
        lista=reactions.listar_reacciones(),
        hechas=session.get("reactions_done", []),
        octeto_msg=octeto.get_octeto_message("reaccion_intro"),
    )


@app.route("/reaction/<reaction_id>")
def reaction_puzzle(reaction_id):
    """Puzle individual: los pasos se muestran barajados."""
    r = reactions.obtener_reaccion(reaction_id)
    if not r:
        return "Reacción no encontrada", 404
    orden = list(range(len(r["pasos"])))
    random.shuffle(orden)
    # Evitar que salga ya ordenado por azar
    if orden == sorted(orden):
        orden.reverse()
    pista = f"🐙 Psst… el primer paso es: «{r['pasos'][0]}». No se lo digas a nadie."
    return views_nuevas.render_reaction_page(
        reaccion=r, orden_barajado=orden,
        octeto_msg=octeto.get_octeto_message("reaccion_intro"),
        pista_octeto=pista,
    )


@app.route("/check_reaction", methods=["POST"])
def check_reaction():
    """Valida el orden de pasos + la pregunta; suma puntos si es correcto."""
    data = request.get_json() or {}
    resultado = reactions.validar_reaccion(
        data.get("id", ""), data.get("orden", []), data.get("respuesta", -1))
    if not resultado.get("ok"):
        return jsonify({"correcto": False,
                        "mensaje": "🐙 Esa reacción no está en mis apuntes…",
                        "mensaje_texto": resultado.get("error", "Error")}), 400

    toasts = []
    if resultado["correcto"]:
        hechas = session.get("reactions_done", [])
        if data["id"] not in hechas:
            session["reactions_done"] = hechas + [data["id"]]
            session["score_reactions"] = (session.get("score_reactions", 0)
                                          + resultado["puntos"])
            session.modified = True
        mensaje = octeto.get_octeto_message("reaccion_correcta")
        texto = f"✅ ¡Correcto! +{resultado['puntos']} puntos."
    else:
        mensaje = octeto.get_octeto_message("reaccion_incorrecta")
        texto = f"❌ {resultado['detalle']}"

    return jsonify({"correcto": resultado["correcto"], "mensaje": mensaje,
                    "mensaje_texto": texto, "fun_fact": resultado["fun_fact"],
                    "toasts": toasts})


# ─────────────────────────────────────────────
# RUTAS NUEVAS v2: GALERÍA Y LOGROS
# ─────────────────────────────────────────────

@app.route("/gallery")
def gallery():
    """Galería con las moléculas completadas y las creaciones del sandbox."""
    entradas = []
    for g in session.get("gallery", []):
        if g.get("tipo") == "desafio":
            m = get_molecule_by_id(g.get("id", ""))
            if not m:
                continue
            entradas.append({
                "tipo": "desafio", "nombre": m["name"], "formula": m["formula"],
                "svg": get_svg(m["svg_key"]),
                "xyz": get_xyz(m["svg_key"], m["atoms"], m["name"]),
                "fun_fact": m["fun_fact"],
            })
        else:  # sandbox
            atoms = g.get("atoms", [])
            entradas.append({
                "tipo": "sandbox",
                "nombre": "Creación propia",
                "formula": g.get("formula", "?"),
                "svg": get_svg(g.get("formula", "?")),   # placeholder con la fórmula
                "xyz": xyz_from_sandbox([{"sym": a["s"], "x": a["x"], "y": a["y"]}
                                         for a in atoms]),
                "fun_fact": "",
            })
    tipo_msg = "galeria" if entradas else "galeria_vacia"
    return views_nuevas.render_gallery_page(
        entradas=entradas,
        octeto_msg=octeto.get_octeto_message(tipo_msg),
        pending_toasts=_sacar_toasts_pendientes(),
    )


@app.route("/achievements")
def achievements_page():
    """Vitrina de logros."""
    desbloqueados = session.get("achievements", [])
    if desbloqueados:
        msg = (f"🐙 Llevas {len(desbloqueados)} de {len(logros_mod.LOGROS)} logros. "
               "Mi vitrina favorita, después de la de conchas.")
    else:
        msg = "🐙 Aún no tienes logros… ¡pero tengo ocho brazos llenos de fe en ti!"
    return views_nuevas.render_achievements_page(
        desbloqueados=desbloqueados,
        octeto_msg=msg,
        pending_toasts=_sacar_toasts_pendientes(),
    )


# ─────────────────────────────────────────────
# RUTAS NUEVAS v2: MISIÓN NARRATIVA
# ─────────────────────────────────────────────

@app.route("/story")
def story():
    """Portada de la misión: muestra intro, progreso o final."""
    total = missions.total_capitulos()
    idx = session.get("mol_index_story", None)
    terminada = idx is not None and idx >= total
    en_curso = idx is not None and 0 < idx < total or (
        idx == 0 and session.get("filled_story_0"))
    return views_nuevas.render_story_page(
        mission=missions.MISSION,
        capitulo_actual=idx or 0, total=total,
        terminada=terminada, en_curso=bool(en_curso),
        octeto_msg=octeto.get_octeto_message("historia"),
    )


@app.route("/story/start")
def story_start():
    """(Re)inicia la misión narrativa y entra al primer capítulo."""
    session["mol_index_story"] = 0
    session["score_story"] = 0
    session["hints_story_0"] = []
    session["filled_story_0"] = {}
    session.modified = True
    return redirect("/game/story/play")


# ─────────────────────────────────────────────
# API NUEVA v2
# ─────────────────────────────────────────────

@app.route("/api/molecule3d/<mol_id>")
def api_molecule3d(mol_id):
    """Estructura 3D (XYZ) de una molécula del juego, por id."""
    m = get_molecule_by_id(mol_id)
    if not m:
        return jsonify({"error": "Molécula no encontrada"}), 404
    return jsonify({"id": m["id"], "name": m["name"],
                    "xyz": get_xyz(m["svg_key"], m["atoms"], m["name"])})


if __name__ == "__main__":
    from config import HOST, PORT, DEBUG
    app.run(debug=DEBUG, host=HOST, port=PORT, use_reloader=DEBUG)
