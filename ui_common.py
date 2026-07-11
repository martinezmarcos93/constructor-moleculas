"""
ui_common.py  ─  Átomos Perdidos v2
Piezas de interfaz compartidas por todas las páginas, generadas desde Python:
  - Bocadillo flotante de Octeto 🐙 (no intrusivo en móvil)
  - Toasts de logros
  - Sonidos generados con Web Audio API (sin archivos externos)
  - Modal del visor 3D (3Dmol.js) y confeti (canvas-confetti), ambos desde CDN
  - Envoltorio de página con navegación para las secciones nuevas
"""

import html as _html

# ── CDNs (solo se incluyen en las páginas que los usan) ──────────────
# 3Dmol.js: licencia BSD-3-Clause. canvas-confetti: licencia ISC.
CDN_3DMOL    = '<script src="https://3Dmol.org/build/3Dmol-min.js" defer></script>'
CDN_CONFETTI = '<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js" defer></script>'


# ── CSS compartido ───────────────────────────────────────────────────

BASE_CSS = """
:root{--bg:#0d0d1a;--surface:#151528;--card:#1e1e38;--border:#2e2e55;
--accent:#7c6af7;--accent2:#4fd1c5;--text:#e8e8f0;--muted:#8888aa;
--success:#4ade80;--error:#f87171;--warn:#fbbf24}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:'Courier New',monospace;min-height:100vh}
.top-nav{background:linear-gradient(135deg,#1a1a3e,#0d1a2e);border-bottom:1px solid var(--border);
padding:10px 16px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.top-nav .logo{font-size:1.15rem;font-weight:bold;text-decoration:none;
background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.top-nav a.nav-link{color:var(--muted);text-decoration:none;font-size:.8rem;padding:5px 10px;border-radius:6px;border:1px solid transparent}
.top-nav a.nav-link:hover{color:var(--text);border-color:var(--border)}
.top-nav a.nav-link.active{color:var(--accent2);border-color:var(--accent2)}
.page-wrap{max-width:1300px;margin:0 auto;padding:16px}
.card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px}
.btn{padding:10px 18px;border:none;border-radius:8px;cursor:pointer;font-family:monospace;
font-weight:bold;font-size:.9rem;transition:all .2s;text-decoration:none;display:inline-block}
.btn:hover{transform:translateY(-1px)}
.btn-primary{background:linear-gradient(135deg,var(--accent),#5a4ad7);color:#fff}
.btn-teal{background:linear-gradient(135deg,var(--accent2),#38b2ac);color:#000}
.btn-ghost{background:var(--card);border:1px solid var(--border);color:var(--text)}
.btn-danger{background:#3a1a1a;border:1px solid #6a2a2a;color:var(--error)}
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
"""

# Bocadillo de Octeto + toasts + modal 3D
WIDGETS_CSS = """
/* ── Octeto 🐙 ── */
.octeto-widget{position:fixed;bottom:14px;right:14px;z-index:900;display:flex;
align-items:flex-end;gap:8px;max-width:min(420px,calc(100vw - 28px));pointer-events:none}
.octeto-bubble{background:#221a3e;border:1px solid var(--accent);border-radius:14px 14px 2px 14px;
padding:10px 32px 10px 14px;font-size:.8rem;line-height:1.45;color:#d8d0ff;position:relative;
box-shadow:0 6px 24px rgba(0,0,0,.5);animation:octeto-in .4s ease;pointer-events:auto}
.octeto-bubble .octeto-close{position:absolute;top:4px;right:6px;background:none;border:none;
color:var(--muted);cursor:pointer;font-size:.85rem;padding:2px;font-family:monospace}
.octeto-avatar{font-size:2rem;filter:drop-shadow(0 2px 6px rgba(124,106,247,.6));
animation:octeto-bob 3s ease-in-out infinite;pointer-events:auto;cursor:pointer;user-select:none}
.octeto-reopen{position:fixed;bottom:14px;right:14px;z-index:900;font-size:1.7rem;background:#221a3e;
border:1px solid var(--accent);border-radius:50%;width:48px;height:48px;cursor:pointer;display:none;
align-items:center;justify-content:center;box-shadow:0 4px 16px rgba(0,0,0,.5)}
@keyframes octeto-in{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@keyframes octeto-bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
@media(max-width:640px){
  .octeto-widget{bottom:8px;right:8px;left:8px;max-width:none}
  .octeto-bubble{font-size:.72rem;padding:8px 28px 8px 10px;flex:1}
  .octeto-avatar{font-size:1.5rem}
}
/* ── Toasts ── */
.toast-zone{position:fixed;top:14px;left:50%;transform:translateX(-50%);z-index:950;
display:flex;flex-direction:column;gap:8px;align-items:center;width:min(440px,calc(100vw - 20px))}
.toast{background:#1a2a1a;border:1px solid var(--success);color:#c8f0c8;border-radius:10px;
padding:10px 16px;font-size:.8rem;box-shadow:0 6px 24px rgba(0,0,0,.55);animation:toast-in .35s ease;width:100%}
.toast.toast-info{background:#221a3e;border-color:var(--accent);color:#d8d0ff}
@keyframes toast-in{from{opacity:0;transform:translateY(-12px)}to{opacity:1;transform:none}}
/* ── Modal 3D ── */
.mol3d-modal{position:fixed;inset:0;z-index:960;background:rgba(5,5,15,.82);display:flex;
align-items:center;justify-content:center;padding:14px}
.mol3d-box{background:var(--card);border:1px solid var(--accent);border-radius:14px;width:min(640px,100%);
display:flex;flex-direction:column;overflow:hidden;box-shadow:0 10px 50px rgba(0,0,0,.7)}
.mol3d-head{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;
border-bottom:1px solid var(--border);color:var(--accent2);font-weight:bold;font-size:.9rem}
.mol3d-head button{background:none;border:1px solid var(--border);color:var(--muted);border-radius:6px;
cursor:pointer;padding:4px 10px;font-family:monospace}
.mol3d-viewer{width:100%;height:min(420px,60vh);position:relative}
.mol3d-tip{padding:8px 14px;font-size:.7rem;color:var(--muted);border-top:1px solid var(--border);text-align:center}
"""


# ── JS compartido ────────────────────────────────────────────────────

SHARED_JS = """
// ═══ Sonidos: tonos generados con Web Audio API (sin archivos) ═══
let _actx = null;
function _audio(){
  if (!_actx) { try { _actx = new (window.AudioContext||window.webkitAudioContext)(); } catch(e){} }
  return _actx;
}
function _tone(freq, dur, type, when, vol){
  const ctx = _audio(); if (!ctx) return;
  const t0 = ctx.currentTime + (when||0);
  const osc = ctx.createOscillator(), g = ctx.createGain();
  osc.type = type||'sine'; osc.frequency.value = freq;
  g.gain.setValueAtTime(vol||0.12, t0);
  g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
  osc.connect(g); g.connect(ctx.destination);
  osc.start(t0); osc.stop(t0 + dur + 0.05);
}
function playPop(){ _tone(420, .09, 'triangle', 0, .18); _tone(640, .06, 'sine', .03, .1); }
function playDing(){ _tone(880, .18, 'sine', 0, .12); _tone(1318, .28, 'sine', .06, .09); }
function playError(){ _tone(180, .22, 'sawtooth', 0, .08); _tone(140, .25, 'sawtooth', .08, .07); }
function playFanfare(){
  [[523,.0],[659,.10],[784,.20],[1047,.32]].forEach(p => _tone(p[0], .22, 'triangle', p[1], .12));
  _tone(1319, .5, 'sine', .46, .1);
}

// ═══ Toasts ═══
function showToast(texto, tipo){
  let zone = document.querySelector('.toast-zone');
  if (!zone){ zone = document.createElement('div'); zone.className='toast-zone'; document.body.appendChild(zone); }
  const t = document.createElement('div');
  t.className = 'toast' + (tipo==='info' ? ' toast-info' : '');
  t.textContent = texto;
  zone.appendChild(t);
  setTimeout(()=>{ t.style.transition='opacity .5s'; t.style.opacity='0'; setTimeout(()=>t.remove(), 550); }, 4200);
}

// ═══ Confeti (si canvas-confetti cargó desde CDN) ═══
function fireConfetti(){
  if (typeof confetti === 'undefined') return;
  confetti({particleCount:110, spread:75, origin:{y:.7}});
  setTimeout(()=>confetti({particleCount:60, angle:60, spread:60, origin:{x:0}}), 220);
  setTimeout(()=>confetti({particleCount:60, angle:120, spread:60, origin:{x:1}}), 380);
}

// ═══ Bocadillo de Octeto: cerrar / reabrir ═══
function octetoCerrar(){
  const w = document.getElementById('octeto-widget');
  const r = document.getElementById('octeto-reopen');
  if (w) w.style.display = 'none';
  if (r) r.style.display = 'flex';
}
function octetoAbrir(){
  const w = document.getElementById('octeto-widget');
  const r = document.getElementById('octeto-reopen');
  if (w) w.style.display = 'flex';
  if (r) r.style.display = 'none';
}
function octetoDecir(texto){
  const b = document.getElementById('octeto-texto');
  if (b){ b.textContent = texto; octetoAbrir(); }
  else { showToast(texto, 'info'); }
}
"""

# Visor 3D con 3Dmol.js. El XYZ viene incrustado desde Python.
MOL3D_JS = """
// ═══ Visor 3D (3Dmol.js desde CDN) ═══
let _viewer3d = null;
function openMol3D(xyz, titulo){
  if (typeof $3Dmol === 'undefined'){
    octetoDecir('🐙 El visor 3D no cargó (¿sin conexión?). Mis tentáculos no llegan tan lejos…');
    return;
  }
  const modal = document.getElementById('mol3d-modal');
  modal.style.display = 'flex';
  document.getElementById('mol3d-title').textContent = titulo || 'Molécula en 3D';
  const box = document.getElementById('mol-viewer');
  box.innerHTML = '';
  _viewer3d = $3Dmol.createViewer(box, {defaultcolors: $3Dmol.rasmolElementColors, backgroundColor: '#0d0d1a'});
  _viewer3d.addModel(xyz, 'xyz');
  _viewer3d.setStyle({}, {stick:{radius:0.14}, sphere:{scale:0.32}});
  _viewer3d.zoomTo();
  _viewer3d.render();
  _viewer3d.spin('y', 0.6);   // rotación suave inicial; el usuario puede arrastrar
}
function closeMol3D(){
  const modal = document.getElementById('mol3d-modal');
  if (_viewer3d){ _viewer3d.spin(false); }
  modal.style.display = 'none';
}
// Cerrar al hacer clic fuera del cuadro
document.addEventListener('click', (e) => {
  const modal = document.getElementById('mol3d-modal');
  if (modal && e.target === modal) closeMol3D();
});
"""


# ── Generadores de fragmentos HTML ───────────────────────────────────

def build_octeto_html(mensaje: str) -> str:
    """Bocadillo flotante de Octeto con su mensaje. Cerrable y reabrible."""
    safe = _html.escape(mensaje).replace("🐙 ", "", 1)
    return f"""
<div class="octeto-widget" id="octeto-widget">
  <div class="octeto-bubble">
    <span id="octeto-texto">{safe}</span>
    <button class="octeto-close" onclick="octetoCerrar()" title="Cerrar">✕</button>
  </div>
  <div class="octeto-avatar" onclick="octetoCerrar()" title="Octeto">🐙</div>
</div>
<button class="octeto-reopen" id="octeto-reopen" onclick="octetoAbrir()" title="Llamar a Octeto">🐙</button>
"""


def build_mol3d_modal_html() -> str:
    """Modal (oculto) del visor 3D. Se abre con openMol3D(xyz, titulo)."""
    return """
<div class="mol3d-modal" id="mol3d-modal" style="display:none">
  <div class="mol3d-box">
    <div class="mol3d-head">
      <span id="mol3d-title">Molécula en 3D</span>
      <button onclick="closeMol3D()">✕ Cerrar</button>
    </div>
    <div id="mol-viewer" class="mol3d-viewer"></div>
    <div class="mol3d-tip">🖱️ Arrastra para rotar · rueda / pellizco para hacer zoom</div>
  </div>
</div>
"""


def build_pending_toasts_js(toasts: list) -> str:
    """JS que muestra los toasts pendientes (logros) al cargar la página."""
    if not toasts:
        return ""
    import json
    return f"""
document.addEventListener('DOMContentLoaded', () => {{
  const pendientes = {json.dumps(toasts, ensure_ascii=False)};
  pendientes.forEach((t, i) => setTimeout(() => {{ showToast(t); }}, 500 + i*900));
  if (pendientes.length) setTimeout(fireConfetti, 600);
}});
"""


NAV_LINKS = [
    ("/",             "🏠 Inicio"),
    ("/sandbox",      "🧪 Sandbox"),
    ("/reactions",    "⚗️ Reacciones"),
    ("/story",        "📖 Historia"),
    ("/gallery",      "🖼️ Galería"),
    ("/achievements", "🏅 Logros"),
]


def build_nav_html(active: str = "") -> str:
    """Barra de navegación superior compartida por las páginas nuevas."""
    links = ""
    for href, label in NAV_LINKS:
        cls = "nav-link active" if href == active else "nav-link"
        links += f'<a class="{cls}" href="{href}">{label}</a>'
    return f"""
<div class="top-nav">
  <a class="logo" href="/">⚗️ Átomos Perdidos</a>
  {links}
</div>
"""


def build_page(title: str, body: str, active_nav: str = "", octeto_msg: str = "",
               extra_css: str = "", extra_js: str = "", extra_head: str = "",
               pending_toasts: list = None, include_3d: bool = False) -> str:
    """
    Envoltorio de página completo para las secciones nuevas.
    Mantiene el espíritu del proyecto: todo el HTML sale de Python.
    """
    head_cdns = CDN_CONFETTI
    mol3d_html = ""
    mol3d_js = ""
    if include_3d:
        head_cdns += "\n" + CDN_3DMOL
        mol3d_html = build_mol3d_modal_html()
        mol3d_js = MOL3D_JS

    octeto_html = build_octeto_html(octeto_msg) if octeto_msg else ""
    toasts_js = build_pending_toasts_js(pending_toasts or [])

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{head_cdns}
{extra_head}
<style>
{BASE_CSS}
{WIDGETS_CSS}
{extra_css}
</style>
</head>
<body>
{build_nav_html(active_nav)}
<div class="page-wrap">
{body}
</div>
{octeto_html}
{mol3d_html}
<script>
{SHARED_JS}
{mol3d_js}
{toasts_js}
{extra_js}
</script>
</body>
</html>"""
