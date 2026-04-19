"""
app.py  –  Átomos Perdidos: El Constructor de Moléculas
Servidor Flask: toda la lógica y generación de HTML ocurre aquí en Python.
"""

from flask import Flask, session, request, jsonify, render_template_string
import json, uuid

from periodic_table import ELEMENTS, ELEMENT_POSITIONS, CATEGORY_COLORS, CATEGORY_LABELS
from molecules import GameSession, MOLECULES, LEVEL_LABELS, get_molecule_by_id
from svg_molecules import get_svg

app = Flask(__name__)
app.secret_key = "atomos_perdidos_secret_2025"

# ─────────────────────────────────────────────
# GENERADOR DE HTML  (Python genera todo el HTML)
# ─────────────────────────────────────────────

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

    # Botón de pista
    hint_btn = (
        f'<button class="btn-hint" onclick="requestHint()" '
        f'{"disabled" if hints_remaining == 0 else ""}>'
        f'💡 Pedir pista ({hints_remaining} restantes)</button>'
        if not completed else ""
    )

    # SVG de la molécula (solo si completada)
    svg_section = ""
    if completed:
        svg_content = get_svg(mol["svg_key"])
        svg_section = f"""
        <div class="completed-section">
            <div class="molecule-svg">{svg_content}</div>
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

    # ── Plantilla HTML completa ───────────────
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Átomos Perdidos 🔬</title>
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
    <button onclick="location.href='/'" style="background:var(--card);border:1px solid var(--border);color:var(--muted);padding:6px 12px;border-radius:6px;cursor:pointer;font-family:monospace;font-size:.8rem">🏠 Inicio</button>
  </div>
</div>

<div class="main">
  <!-- Molécula incompleta -->
  <div class="mol-section">
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

<script>
// ── Estado del juego (generado por Python, consumido por JS) ──
const GAME = {game_data};

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
}});
</script>
</body>
</html>"""
    return html


def render_home():
    """Página de inicio generada por Python."""
    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Átomos Perdidos 🔬</title>
<style>
:root{--bg:#0d0d1a;--surface:#151528;--card:#1e1e38;--border:#2e2e55;--accent:#7c6af7;--accent2:#4fd1c5;--text:#e8e8f0;--muted:#8888aa}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:'Courier New',monospace;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px}
.hero{text-align:center;margin-bottom:40px}
.title{font-size:3rem;font-weight:bold;background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.2}
.subtitle{color:var(--muted);font-size:1rem;margin-top:10px;max-width:500px}
.levels{display:flex;gap:20px;flex-wrap:wrap;justify-content:center}
.level-card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:28px 36px;text-align:center;cursor:pointer;transition:all .3s;text-decoration:none;color:var(--text);min-width:200px}
.level-card:hover{transform:translateY(-6px);border-color:var(--accent);box-shadow:0 8px 30px rgba(124,106,247,.25)}
.level-icon{font-size:3rem;margin-bottom:12px}
.level-name{font-size:1.4rem;font-weight:bold;margin-bottom:8px}
.level-desc{font-size:.8rem;color:var(--muted);line-height:1.5}
.easy-card .level-name{color:#4ade80}
.medium-card .level-name{color:#fbbf24}
.hard-card .level-name{color:#f87171}
.footer{margin-top:40px;color:var(--muted);font-size:.75rem;text-align:center}
.atoms-bg{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;overflow:hidden;z-index:-1}
.float-atom{position:absolute;border-radius:50%;opacity:.06;animation:float linear infinite}
@keyframes float{0%{transform:translateY(100vh) rotate(0deg)}100%{transform:translateY(-200px) rotate(360deg)}}
</style>
</head>
<body>
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
<div class="footer">
  <p>118 elementos · Configuraciones electrónicas completas · 20 moléculas</p>
  <p style="margin-top:4px">Motor: Python + Flask · Tabla periódica generada dinámicamente</p>
</div>
</body>
</html>"""


def render_finished_page(level: str, score: int):
    total = len(MOLECULES.get(level, []))
    max_score = total * 10
    pct = int(score / max_score * 100) if max_score else 0
    stars = "⭐" * (1 + (pct >= 50) + (pct >= 80) + (pct >= 100))
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>¡Completado! — Átomos Perdidos</title>
<style>
:root{{--bg:#0d0d1a;--card:#1e1e38;--border:#2e2e55;--accent:#7c6af7;--accent2:#4fd1c5;--text:#e8e8f0;--muted:#8888aa}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:'Courier New',monospace;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:40px;text-align:center;max-width:500px;width:100%}}
.big-stars{{font-size:3rem;margin-bottom:16px}}
h1{{font-size:2rem;background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}}
.score{{font-size:3rem;font-weight:bold;color:var(--accent2);margin:20px 0}}
.sub{{color:var(--muted);font-size:.9rem;margin-bottom:28px}}
.btns{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}}
a.btn{{padding:12px 24px;border-radius:10px;text-decoration:none;font-family:monospace;font-weight:bold;font-size:.95rem;transition:all .2s}}
a.btn:hover{{transform:translateY(-2px)}}
.btn-retry{{background:var(--accent);color:#fff}}
.btn-home{{background:var(--card);border:1px solid var(--border);color:var(--text)}}
</style>
</head>
<body>
<div class="card">
  <div class="big-stars">{stars}</div>
  <h1>¡Nivel completado!</h1>
  <div class="score">{score} pts</div>
  <div class="sub">Nivel {LEVEL_LABELS.get(level,'')} — {total} moléculas — Máximo posible: {max_score} pts<br>Puntuación: {pct}%</div>
  <div class="btns">
    <a href="/game/{level}" class="btn btn-retry">🔁 Repetir nivel</a>
    <a href="/" class="btn btn-home">🏠 Inicio</a>
  </div>
</div>
</body>
</html>"""


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
    from flask import redirect
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
            session.modified = True
            return jsonify({"reload": True, "completed": True})
        return jsonify({"reload": True})
    else:
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





if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
