"""
views_nuevas.py  ─  Átomos Perdidos v2
Páginas nuevas generadas 100 % desde Python (mismo espíritu que app.py):
  - /sandbox      → laboratorio libre
  - /reactions    → listado de puzles de reacción
  - /reaction/<id>→ puzle individual (ordenar pasos + pregunta)
  - /gallery      → galería de moléculas completadas/guardadas
  - /achievements → vitrina de logros
  - /story        → misión narrativa
Los builders reciben los datos ya extraídos de la sesión: no tocan Flask.
"""

import json
import html as _html

from periodic_table import ELEMENTS, ELEMENT_POSITIONS, CATEGORY_COLORS
from svg_molecules import get_svg
from molecule_3d import get_xyz, xyz_from_sandbox
from achievements import LOGROS
from ui_common import build_page


# ── Tabla periódica compacta y clickeable (para el sandbox) ──────────

def build_mini_table_html(onclick_fn: str = "sbSelect(this)") -> str:
    """Tabla periódica en miniatura; cada celda llama a `onclick_fn`."""
    grid = {}
    for z, pos in ELEMENT_POSITIONS.items():
        grid[pos] = z

    rows = []
    for row in range(1, 11):
        cells = ""
        for col in range(1, 19):
            z = grid.get((row, col))
            if z:
                el = ELEMENTS[z]
                color = CATEGORY_COLORS.get(el["category"], "#999")
                cells += (
                    f'<div class="mini-el" data-symbol="{el["symbol"]}" '
                    f'data-name="{el["name"]}" data-valence="{el["valence"]}" '
                    f'style="background:{color}25;border-color:{color}55" '
                    f'onclick="{onclick_fn}" '
                    f'title="{el["name"]} · valencia {el["valence"]}">'
                    f'{el["symbol"]}</div>'
                )
            else:
                cells += '<div class="mini-el mini-empty"></div>'
        rows.append(f'<div class="mini-row">{cells}</div>')
    return "\n".join(rows)


MINI_TABLE_CSS = """
.mini-row{display:flex;gap:1px;margin-bottom:1px}
.mini-el{width:24px;height:24px;font-size:9px;font-weight:bold;display:flex;align-items:center;
justify-content:center;border:1px solid transparent;border-radius:3px;cursor:pointer;
color:var(--text);flex-shrink:0;transition:transform .1s;user-select:none}
.mini-el:hover{transform:scale(1.3);z-index:5;border-color:#fff!important}
.mini-el.selected{outline:2px solid var(--accent2);transform:scale(1.15)}
.mini-empty{background:transparent!important;border-color:transparent!important;pointer-events:none}
"""


# ═════════════════════════════════════════════════════════════════════
#  SANDBOX
# ═════════════════════════════════════════════════════════════════════

SANDBOX_CSS = MINI_TABLE_CSS + """
.sb-layout{display:grid;grid-template-columns:1fr 480px;gap:12px}
@media(max-width:1000px){.sb-layout{grid-template-columns:1fr}}
.sb-lienzo-wrap{position:relative}
#sb-lienzo{position:relative;background:#0a0a18;border:1px dashed var(--border);border-radius:12px;
height:480px;overflow:hidden;cursor:crosshair;touch-action:manipulation}
#sb-bonds{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.sb-atom{position:absolute;width:46px;height:46px;margin:-23px 0 0 -23px;border-radius:50%;
display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:.95rem;
border:2px solid rgba(255,255,255,.35);cursor:pointer;user-select:none;
box-shadow:0 3px 10px rgba(0,0,0,.5);animation:sb-pop .18s ease}
.sb-atom.sb-marked{outline:3px solid var(--accent2)}
@keyframes sb-pop{from{transform:scale(.3)}to{transform:scale(1)}}
.sb-tools{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}
.sb-tool{padding:8px 14px;border-radius:8px;border:1px solid var(--border);background:var(--card);
color:var(--muted);cursor:pointer;font-family:monospace;font-size:.8rem}
.sb-tool.active{border-color:var(--accent2);color:var(--accent2)}
.sb-panel{display:flex;flex-direction:column;gap:10px}
.sb-table-box{overflow-x:auto}
.sb-formula{font-size:1.3rem;color:var(--accent2);font-weight:bold;min-height:1.6em}
.sb-sel-info{font-size:.8rem;color:var(--muted)}
#sb-validacion{min-height:1.5em;margin-top:6px}
#sb-validacion[data-state="ok"]{color:var(--success)}
#sb-validacion[data-state="error"]{color:var(--error)}
"""

SANDBOX_JS = r"""
// ═══ Estado del sandbox ═══
let sbAtoms = [];            // {id, sym, x, y, valence}
let sbBonds = [];            // {a:idA,b:idB,order:1}
let sbBondOrder = 1;
let sbNextId = 1;
let sbElemento = null;       // elemento seleccionado en la mini-tabla
let sbModo = 'colocar';      // colocar | enlazar | borrar
let sbEnlaceOrigen = null;   // primer átomo clickeado en modo enlazar
const AUTO_BOND_DIST = 75;   // px: enlace automático si se coloca cerca

function sbSelect(el){
  document.querySelectorAll('.mini-el.selected').forEach(e => e.classList.remove('selected'));
  el.classList.add('selected');
  sbElemento = {sym: el.dataset.symbol, name: el.dataset.name, valence: parseInt(el.dataset.valence)};
  document.getElementById('sb-sel').textContent =
    sbElemento.sym + ' — ' + sbElemento.name + ' (valencia ' + sbElemento.valence + ')';
  sbSetModo('colocar');
}

function sbSetModo(m){
  sbModo = m; sbEnlaceOrigen = null;
  document.querySelectorAll('.sb-tool[data-modo]').forEach(b =>
    b.classList.toggle('active', b.dataset.modo === m));
  sbRepintar();
}

function sbClickLienzo(ev){
  if (sbModo !== 'colocar' || !sbElemento) {
    if (!sbElemento && sbModo === 'colocar') octetoDecir('🐙 Primero elige un elemento de la tabla, ¡mis tentáculos no adivinan!');
    return;
  }
  const rect = document.getElementById('sb-lienzo').getBoundingClientRect();
  const x = ev.clientX - rect.left, y = ev.clientY - rect.top;
  const atomo = {id: sbNextId++, sym: sbElemento.sym, x: x, y: y, valence: sbElemento.valence};
  sbAtoms.push(atomo);
  // Enlace automático con átomos cercanos
  sbAtoms.forEach(a => {
    if (a.id !== atomo.id && Math.hypot(a.x - x, a.y - y) < AUTO_BOND_DIST){
      sbBonds.push({a:a.id, b:atomo.id, order:1});
    }
  });
  playPop();
  sbAvisarValencia(atomo);
  sbRepintar();
  sbValidar();
}

function sbClickAtomo(ev, id){
  ev.stopPropagation();
  const atomo = sbAtoms.find(a => a.id === id);
  if (sbModo === 'borrar'){
    sbAtoms = sbAtoms.filter(a => a.id !== id);
    sbBonds = sbBonds.filter(b => b.a !== id && b.b !== id);
    sbRepintar();
    sbValidar();
    return;
  }
  if (sbModo === 'enlazar'){
    if (sbEnlaceOrigen === null){
      sbEnlaceOrigen = id;
    } else if (sbEnlaceOrigen !== id){
      const ya = sbBonds.some(b => (b.a===sbEnlaceOrigen && b.b===id) || (b.b===sbEnlaceOrigen && b.a===id));
      if (!ya){
        sbBonds.push({a:sbEnlaceOrigen, b:id, order:sbBondOrder});
        playPop();
        sbAvisarValencia(atomo);
      }
      sbEnlaceOrigen = null;
    }
    sbRepintar();
    sbValidar();
  }
}

function sbEnlacesDe(id){ return sbBonds.filter(b => b.a===id || b.b===id).reduce((n,b) => n + b.order, 0); }
function sbSetBondOrder(order){ sbBondOrder=order; document.querySelectorAll('.sb-order').forEach(b=>b.classList.toggle('active',parseInt(b.dataset.order)===order)); }
function sbCiclarEnlace(ev,a,b){ ev.stopPropagation(); const bond=sbBonds.find(x=>(x.a===a&&x.b===b)||(x.a===b&&x.b===a)); if(bond){bond.order=bond.order>=3?1:bond.order+1; sbValidar(); sbRepintar();} }

// Octeto avisa (pero no impide) si se supera la valencia
function sbValidar(){ fetch('/api/structure/validate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({atoms:sbAtoms.map(a=>({id:String(a.id),symbol:a.sym})),bonds:sbBonds.map(b=>({a:String(b.a),b:String(b.b),order:b.order}))})}).then(r=>r.json()).then(data=>{const box=document.getElementById('sb-validacion');if(!box)return;if(!data.ok){box.textContent='⚠️ '+data.error;return;}const e=(data.issues||[]).find(i=>i.severity==='error');box.textContent=data.valid?'✓ Estructura válida · '+data.formula+(data.vsepr&&data.vsepr.supported?' · '+data.vsepr.geometry:''):'✕ '+(e?e.message:'Estructura por corregir.');box.dataset.state=data.valid?'ok':'error';}).catch(()=>{}); }

function sbAvisarValencia(atomo){
  if (atomo && atomo.valence > 0 && sbEnlacesDe(atomo.id) > atomo.valence){
    octetoDecir(FRASES_VALENCIA[Math.floor(Math.random()*FRASES_VALENCIA.length)]);
    playError();
  }
}

function sbRepintar(){
  const lienzo = document.getElementById('sb-lienzo');
  lienzo.querySelectorAll('.sb-atom').forEach(n => n.remove());
  const svg = document.getElementById('sb-bonds');
  svg.innerHTML = sbBonds.map(b => {
    const a1 = sbAtoms.find(a => a.id === b.a), a2 = sbAtoms.find(a => a.id === b.b);
    if (!a1 || !a2) return '';
    return Array.from({length:b.order},(_,k)=>{const dx=a2.x-a1.x,dy=a2.y-a1.y,len=Math.hypot(dx,dy),off=(k-(b.order-1)/2)*5,ox=-dy/len*off,oy=dx/len*off;return '<line x1="'+(a1.x+ox)+'" y1="'+(a1.y+oy)+'" x2="'+(a2.x+ox)+'" y2="'+(a2.y+oy)+'" stroke="#8888aa" stroke-width="3" stroke-linecap="round"/>';}).join('');
  }).join('');
  sbAtoms.forEach(a => {
    const d = document.createElement('div');
    d.className = 'sb-atom' + (a.id === sbEnlaceOrigen ? ' sb-marked' : '');
    d.style.left = a.x + 'px'; d.style.top = a.y + 'px';
    d.style.background = COLOR_ATOMOS[a.sym] || '#8888aa';
    d.style.color = '#111';
    d.textContent = a.sym;
    d.onclick = (ev) => sbClickAtomo(ev, a.id);
    lienzo.appendChild(d);
  });
  document.getElementById('sb-contador').textContent =
    sbAtoms.length + ' átomos · ' + sbBonds.length + ' enlaces';
}

function sbLimpiar(){
  sbAtoms = []; sbBonds = []; sbEnlaceOrigen = null;
  document.getElementById('sb-formula').textContent = '';
  sbRepintar();
  octetoDecir('🐙 Lienzo limpio. Como mi conciencia. Bueno, casi.');
}

function sbCalcularFormula(cb){
  if (!sbAtoms.length){ octetoDecir('🐙 No hay átomos que contar. ¡El vacío no tiene fórmula!'); return; }
  fetch('/sandbox/formula', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({simbolos: sbAtoms.map(a => a.sym)})
  }).then(r => r.json()).then(data => {
    document.getElementById('sb-formula').textContent = data.formula;
    octetoDecir(data.mensaje);
    playDing();
    if (cb) cb(data.formula);
  });
}

function sbGuardar(){
  if (!sbAtoms.length){ octetoDecir('🐙 Guardar la nada sería muy zen, pero no. Coloca algún átomo.'); return; }
  sbCalcularFormula(formula => {
    fetch('/sandbox/save', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({atoms: sbAtoms.map(a => ({id:a.id, s:a.sym, x:Math.round(a.x), y:Math.round(a.y)})), bonds: sbBonds})
    }).then(r => r.json()).then(data => {
      octetoDecir(data.mensaje);
      (data.toasts || []).forEach((t,i) => setTimeout(() => showToast(t), 400 + i*900));
      if ((data.toasts || []).length) fireConfetti();
    });
  });
}

function sbExperimentar(id){
  const box=document.getElementById('sb-experimento');
  if(!box) return;
  box.dataset.id=id;
  fetch('/api/experiments/'+id).then(r=>r.json()).then(data=>{
    if(!data.ok){box.textContent='⚠️ '+data.error;return;}
    const e=data.experiment;
    const controls=e.controls.map(v=>'<label style="display:block;margin:6px 0">'+v.label+' <input id="exp-'+v.id+'" type="number" min="'+(v.minimum===null?'':v.minimum)+'" max="'+(v.maximum===null?'':v.maximum)+'" step="'+(v.step===null?'':v.step)+'" value="'+(v.minimum===null?'':v.minimum)+'"></label>').join('');
    box.innerHTML='<strong>'+e.title+'</strong><p>'+e.hypothesis_prompt+'</p>'+controls<textarea id="sb-observacion" placeholder="Escribe qué observas antes de ejecutar el experimento..." style="width:100%;min-height:70px;margin:8px 0"></textarea>'+
      '<div class="sb-exp-opciones">'+e.prediction_options.map(x=>'<button class="btn btn-ghost" onclick="sbEjecutarExperimento(\\''+id+'\\',\\''+x+'\\')">'+x.replaceAll('_',' ')+'</button>').join(' ')+'</div>';
  });
}
function sbEjecutarExperimento(id,prediction){
  const box=document.getElementById('sb-experimento');
  const obs=(document.getElementById('sb-observacion')||{}).value||'';
  const payload={prediction,observations:obs.trim()?[obs.trim()]:[],variables:{}};
  ['temperature','reactant_amount','oxygen_amount','first_amount','second_amount','first_moles','second_moles'].forEach(k=>{const el=document.getElementById('exp-'+k);if(el&&el.value!=='')payload.variables[k]=Number(el.value);});
  if(id==='polaridad_agua'){
    payload.atoms=sbAtoms.map(a=>({id:String(a.id),symbol:a.sym}));
    payload.bonds=sbBonds.map(b=>({a:String(b.a),b:String(b.b),order:b.order}));
  } else if(id==='masa_molar'){
    payload.formulas=['H₂O','CO₂'];
  } else if(id==='rendimiento_reaccion'){
    payload.equation={reactants:['H2','O2'],products:['H2O']};
  } else if(id==='conservacion_materia'){
    payload.equation={reactants:['H2','O2'],products:['H2O']};
  }
  fetch('/api/experiments/'+id+'/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
    .then(r=>r.json()).then(data=>{
      if(!data.ok){box.textContent='⚠️ '+data.error;return;}
      const run=data.run;
      const result=run.result||{};
      let detail='Puntuación: '+run.score+'/100. ';
      if(id==='polaridad_agua') detail+=(result.polar?'El resultado es POLAR. ':'El resultado es NO POLAR. ')+(run.prediction=== 'polar' ? 'Tu predicción fue correcta.':'Tu predicción fue incorrecta.');
      if(id==='masa_molar') detail+='Mayor masa molar: '+(result.greater==='first'?'primera':'segunda')+' fórmula.';
      if(id==='conservacion_materia') detail+='Ecuación balanceada: '+result.equation;
      if(id==='rendimiento_reaccion') detail+='Limitante: '+result.limiting_reagent+' · Producto teórico: '+result.products[0].theoretical_moles+' mol · Exceso: '+(result.excess_reagents.join(', ')||'ninguno');
      box.innerHTML='<strong>Resultado</strong><p>'+detail+'</p><small>La puntuación premia tanto acertar la predicción como registrar una observación.</small>';
    });
}
function sbCargarExperimentos(){
  const box=document.getElementById('sb-experimentos');
  if(!box) return;
  fetch('/api/experiments').then(r=>r.json()).then(data=>{
    box.innerHTML=data.experiments.map(e=>'<button class="btn btn-ghost" onclick="sbExperimentar(\\''+e.id+'\\')">🧪 '+e.title+'</button>').join(' ');
  });
}

function sbAnalizar(){
  if(!sbAtoms.length){ octetoDecir('🐙 Primero construye una molécula.'); return; }
  sbValidar();
  fetch('/api/structure/validate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({
    atoms:sbAtoms.map(a=>({id:String(a.id),symbol:a.sym})),
    bonds:sbBonds.map(b=>({a:String(b.a),b:String(b.b),order:b.order}))
  })}).then(r=>r.json()).then(data=>{
    const box=document.getElementById('sb-analisis');
    if(!data.ok){box.textContent='⚠️ '+data.error;return;}
    const parts=['Fórmula: '+data.formula];
    if(data.vsepr && data.vsepr.supported) parts.push('Geometría: '+data.vsepr.geometry);
    fetch('/api/stoichiometry/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({formula:data.formula})})
      .then(r=>r.json()).then(st=>{
        if(st.ok) parts.push('Masa molar: '+st.molar_mass+' g/mol');
        return fetch('/api/polarity/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({
          atoms:sbAtoms.map(a=>({id:String(a.id),symbol:a.sym})),
          bonds:sbBonds.map(b=>({a:String(b.a),b:String(b.b),order:b.order}))
        })});
      }).then(r=>r.json()).then(pol=>{
        if(pol.ok && pol.polar !== undefined) parts.push(pol.polar?'Polar: sí':'Polar: no');
        box.textContent=parts.join(' · ');
      });
  });
}

sbCargarExperimentos();

function sbVer3D(){
  if (!sbAtoms.length){ octetoDecir('🐙 Primero construye algo, luego lo giramos en 3D.'); return; }
  fetch('/sandbox/xyz', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({atoms: sbAtoms.map(a => ({s:a.sym, x:a.x, y:a.y}))})
  }).then(r => r.json()).then(data => openMol3D(data.xyz, 'Tu creación en 3D'));
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('sb-lienzo').addEventListener('click', sbClickLienzo);
  sbRepintar();
});
"""


def render_sandbox_page(octeto_msg: str, frases_valencia: list,
                        colores_atomos: dict) -> str:
    """Página del modo sandbox (libertad creativa)."""
    tabla = build_mini_table_html()
    body = f"""
<h2 style="margin-bottom:4px">🧪 Sandbox — Libertad creativa</h2>
<p style="color:var(--muted);font-size:.8rem;margin-bottom:12px">
Elige un elemento, haz clic en el lienzo para colocarlo. Los átomos cercanos se
enlazan solos; usa la herramienta <b>Enlazar</b> para unirlos a mano.
Aquí la valencia es solo una sugerencia (Octeto protestará igual).</p>

<div class="sb-layout">
  <div class="sb-lienzo-wrap">
    <div class="sb-tools">
      <button class="sb-tool active" data-modo="colocar" onclick="sbSetModo('colocar')">⚛️ Colocar</button>
      <button class="sb-tool" data-modo="enlazar" onclick="sbSetModo('enlazar')">🔗 Enlazar</button>
      <button class="sb-tool sb-order active" data-order="1" onclick="sbSetBondOrder(1)">— Simple</button>
      <button class="sb-tool sb-order" data-order="2" onclick="sbSetBondOrder(2)">═ Doble</button>
      <button class="sb-tool sb-order" data-order="3" onclick="sbSetBondOrder(3)">≡ Triple</button>
      <button class="sb-tool" data-modo="borrar" onclick="sbSetModo('borrar')">🧽 Borrar átomo</button>
      <span class="sb-sel-info" id="sb-contador">0 átomos · 0 enlaces</span>
    </div>
    <div id="sb-lienzo">
      <svg id="sb-bonds"></svg>
    </div>
    <div class="sb-tools" style="margin-top:12px">
      <button class="btn btn-danger" onclick="sbLimpiar()">🗑️ Limpiar todo</button>
      <button class="btn btn-primary" onclick="sbCalcularFormula()">🧮 Calcular fórmula</button>
      <button class="btn btn-ghost" onclick="sbAnalizar()">🔬 Analizar estructura</button>
      <button class="btn btn-teal" onclick="sbGuardar()">💾 Guardar molécula</button>
      <button class="btn btn-ghost" onclick="sbVer3D()">🔭 Ver en 3D</button>
    </div>
    <div class="sb-formula" id="sb-formula"></div>
    <div class="sb-sel-info" id="sb-validacion"></div>
    <div class="sb-sel-info" id="sb-analisis"></div>
    <div class="sb-sel-info" id="sb-experimentos"></div>
    <div class="sb-sel-info" id="sb-experimento"></div>
  </div>

  <div class="sb-panel">
    <div class="card">
      <div style="font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:2px;margin-bottom:6px">
        Elemento seleccionado</div>
      <div class="sb-sel-info" id="sb-sel">— haz clic en la tabla —</div>
    </div>
    <div class="card sb-table-box">
      <div style="font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:2px;margin-bottom:8px">
        Tabla periódica</div>
      {tabla}
    </div>
  </div>
</div>
"""
    extra_js = (
        "const FRASES_VALENCIA = " + json.dumps(frases_valencia, ensure_ascii=False) + ";\n"
        "const COLOR_ATOMOS = " + json.dumps(colores_atomos) + ";\n"
        + SANDBOX_JS
    )
    return build_page(
        title="Sandbox — Átomos Perdidos 🧪",
        body=body, active_nav="/sandbox", octeto_msg=octeto_msg,
        extra_css=SANDBOX_CSS, extra_js=extra_js, include_3d=True,
    )


# ═════════════════════════════════════════════════════════════════════
#  PUZLES DE REACCIÓN
# ═════════════════════════════════════════════════════════════════════

REACTIONS_CSS = """
.rx-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px;margin-top:14px}
.rx-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:18px;
text-decoration:none;color:var(--text);transition:all .25s;display:block}
.rx-card:hover{transform:translateY(-4px);border-color:var(--accent)}
.rx-eq{color:var(--accent2);font-weight:bold;margin:8px 0}
.rx-meta{font-size:.72rem;color:var(--muted)}
.rx-done{color:var(--success);font-size:.75rem;font-weight:bold}
/* puzle individual */
.rx-steps{display:flex;flex-direction:column;gap:8px;margin:14px 0}
.rx-step{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:10px 12px;
display:flex;align-items:center;gap:10px;font-size:.82rem}
.rx-step .rx-mover{display:flex;flex-direction:column;gap:2px}
.rx-step button{background:var(--card);border:1px solid var(--border);color:var(--muted);border-radius:5px;
cursor:pointer;font-family:monospace;padding:1px 8px;font-size:.75rem}
.rx-step button:hover{color:var(--accent2);border-color:var(--accent2)}
.rx-num{color:var(--accent);font-weight:bold;min-width:20px}
.rx-question{margin:16px 0}
.rx-question label{display:block;padding:8px 10px;border:1px solid var(--border);border-radius:8px;
margin-bottom:6px;cursor:pointer;font-size:.82rem}
.rx-question label:hover{border-color:var(--accent)}
.rx-result{margin-top:14px;padding:12px;border-radius:10px;font-size:.85rem;display:none;border:1px solid}
.rx-result.ok{background:#0a2a0a;border-color:var(--success);color:var(--success);display:block}
.rx-result.err{background:#2a0a0a;border-color:var(--error);color:var(--error);display:block}
.rx-fact{margin-top:10px;background:#0a1a2a;border:1px solid #1a3a5a;border-radius:10px;padding:12px;
font-size:.8rem;color:var(--muted);display:none}
"""

REACTION_JS = r"""
// Mueve un paso arriba/abajo en la lista
function rxMover(btn, delta){
  const step = btn.closest('.rx-step');
  const lista = document.getElementById('rx-steps');
  const items = Array.from(lista.children);
  const i = items.indexOf(step);
  const j = i + delta;
  if (j < 0 || j >= items.length) return;
  if (delta < 0) lista.insertBefore(step, items[j]);
  else lista.insertBefore(items[j], step);
  rxRenumerar();
}
function rxRenumerar(){
  Array.from(document.querySelectorAll('#rx-steps .rx-num')).forEach((n, i) => n.textContent = (i+1) + '.');
}
function rxPista(){
  octetoDecir(RX_PISTA);
}
function rxComprobar(){
  const orden = Array.from(document.querySelectorAll('#rx-steps .rx-step')).map(s => parseInt(s.dataset.orig));
  const sel = document.querySelector('input[name="rx-opcion"]:checked');
  if (!sel){ octetoDecir('🐙 Te falta responder la pregunta de abajo, ¡no me dejes con la intriga!'); return; }
  fetch('/check_reaction', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({id: RX_ID, orden: orden, respuesta: parseInt(sel.value)})
  }).then(r => r.json()).then(data => {
    const res = document.getElementById('rx-result');
    res.className = 'rx-result ' + (data.correcto ? 'ok' : 'err');
    res.textContent = data.mensaje_texto;
    octetoDecir(data.mensaje);
    if (data.correcto){
      playFanfare(); fireConfetti();
      const fact = document.getElementById('rx-fact');
      fact.style.display = 'block';
      fact.textContent = '🔬 ' + data.fun_fact;
      document.getElementById('rx-btn-check').disabled = true;
      (data.toasts || []).forEach((t,i) => setTimeout(() => showToast(t), 600 + i*900));
    } else {
      playError();
    }
  });
}
"""


def render_reactions_page(lista: list, hechas: list, octeto_msg: str) -> str:
    """Listado de puzles de reacción."""
    cards = ""
    for r in lista:
        done = ('<span class="rx-done">✔ Resuelta</span>'
                if r["id"] in hechas else
                f'<span class="rx-meta">🏆 {r["puntos"]} pts</span>')
        cards += f"""
<a class="rx-card" href="/reaction/{r['id']}">
  <div style="font-weight:bold">{r['titulo']}</div>
  <div class="rx-eq">{r['reactivos']} → {r['producto']}</div>
  <div class="rx-meta">Dificultad: {r['dificultad']}</div>
  {done}
</a>"""
    body = f"""
<h2>⚗️ Camino de Reacción</h2>
<p style="color:var(--muted);font-size:.8rem;margin-top:4px">
Ordena los pasos de reacciones químicas reales y responde la pregunta clave.</p>
<div class="rx-grid">{cards}</div>
"""
    return build_page(
        title="Puzles de Reacción — Átomos Perdidos ⚗️",
        body=body, active_nav="/reactions", octeto_msg=octeto_msg,
        extra_css=REACTIONS_CSS,
    )


def render_reaction_page(reaccion: dict, orden_barajado: list,
                         octeto_msg: str, pista_octeto: str) -> str:
    """Puzle individual: pasos barajados con botones ↑/↓ + pregunta."""
    steps_html = ""
    for pos, orig_idx in enumerate(orden_barajado):
        texto = _html.escape(reaccion["pasos"][orig_idx])
        steps_html += f"""
<div class="rx-step" data-orig="{orig_idx}">
  <div class="rx-mover">
    <button onclick="rxMover(this,-1)" title="Subir">▲</button>
    <button onclick="rxMover(this,1)" title="Bajar">▼</button>
  </div>
  <span class="rx-num">{pos + 1}.</span>
  <span>{texto}</span>
</div>"""

    opciones_html = ""
    for i, op in enumerate(reaccion["opciones"]):
        opciones_html += (f'<label><input type="radio" name="rx-opcion" value="{i}"> '
                          f'{_html.escape(op)}</label>')

    body = f"""
<a href="/reactions" style="color:var(--muted);font-size:.8rem;text-decoration:none">← Volver a los puzles</a>
<h2 style="margin-top:8px">{reaccion['titulo']}</h2>
<div class="rx-eq" style="font-size:1.2rem">{reaccion['reactivos']} → {reaccion['producto']}</div>
<p style="color:var(--muted);font-size:.85rem;margin:10px 0">{reaccion['descripcion']}</p>

<div class="card">
  <h3 style="font-size:.8rem;color:var(--muted);text-transform:uppercase;letter-spacing:2px">
    1) Ordena los pasos con ▲ ▼</h3>
  <div class="rx-steps" id="rx-steps">{steps_html}</div>

  <h3 style="font-size:.8rem;color:var(--muted);text-transform:uppercase;letter-spacing:2px">
    2) {_html.escape(reaccion['pregunta'])}</h3>
  <div class="rx-question">{opciones_html}</div>

  <button class="btn btn-teal" id="rx-btn-check" onclick="rxComprobar()">✅ Comprobar reacción</button>
  <button class="btn btn-ghost" onclick="rxPista()">🐙 Pista de Octeto</button>
  <div class="rx-result" id="rx-result"></div>
  <div class="rx-fact" id="rx-fact"></div>
</div>
"""
    extra_js = (
        "const RX_ID = " + json.dumps(reaccion["id"]) + ";\n"
        "const RX_PISTA = " + json.dumps(pista_octeto, ensure_ascii=False) + ";\n"
        + REACTION_JS
    )
    return build_page(
        title=f"{reaccion['titulo']} — Átomos Perdidos ⚗️",
        body=body, active_nav="/reactions", octeto_msg=octeto_msg,
        extra_css=REACTIONS_CSS, extra_js=extra_js,
    )


# ═════════════════════════════════════════════════════════════════════
#  GALERÍA
# ═════════════════════════════════════════════════════════════════════

GALLERY_CSS = """
.gal-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;margin-top:14px}
.gal-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:14px;
display:flex;flex-direction:column;gap:8px;align-items:center;text-align:center}
.gal-card svg{max-width:100%;height:auto}
.gal-name{font-weight:bold;color:var(--accent2);font-size:.9rem}
.gal-formula{color:var(--muted);font-size:.8rem}
.gal-tag{font-size:.65rem;padding:2px 8px;border-radius:10px;border:1px solid var(--border);color:var(--muted)}
.gal-tag.sandbox{border-color:var(--warn);color:var(--warn)}
.gal-fact{font-size:.7rem;color:var(--muted);line-height:1.4;max-height:64px;overflow:hidden}
.gal-empty{text-align:center;color:var(--muted);padding:60px 20px;font-size:.9rem}
"""


def render_gallery_page(entradas: list, octeto_msg: str,
                        pending_toasts: list) -> str:
    """
    Galería. `entradas` viene preparada desde app.py:
    [{tipo, nombre, formula, svg, xyz, fun_fact}, …]
    """
    if not entradas:
        cuerpo = """<div class="gal-empty">
        La galería está vacía…<br><br>
        Completa moléculas en los niveles o guarda creaciones del sandbox
        para llenar tu vitrina. 🧪</div>"""
    else:
        cards = ""
        for i, e in enumerate(entradas):
            tag = ('<span class="gal-tag sandbox">🧪 sandbox</span>'
                   if e["tipo"] == "sandbox" else
                   '<span class="gal-tag">🏆 desafío</span>')
            fact = f'<div class="gal-fact">{_html.escape(e["fun_fact"][:150])}…</div>' if e.get("fun_fact") else ""
            btn3d = (f'<button class="btn btn-ghost" style="font-size:.75rem;padding:6px 12px" '
                     f'onclick=\'openMol3D(GAL_XYZ[{i}], {json.dumps(e["nombre"], ensure_ascii=False)})\'>'
                     f'🔭 Ver en 3D</button>') if e.get("xyz") else ""
            cards += f"""
<div class="gal-card">
  {tag}
  <div>{e['svg']}</div>
  <div class="gal-name">{_html.escape(e['nombre'])}</div>
  <div class="gal-formula">{e['formula']}</div>
  {fact}
  {btn3d}
</div>"""
        cuerpo = f'<div class="gal-grid">{cards}</div>'

    body = f"""
<h2>🖼️ Galería de Moléculas</h2>
<p style="color:var(--muted);font-size:.8rem;margin-top:4px">
Tu colección: moléculas completadas en los desafíos y creaciones del sandbox.</p>
{cuerpo}
"""
    xyz_list = [e.get("xyz", "") for e in entradas]
    extra_js = "const GAL_XYZ = " + json.dumps(xyz_list) + ";\n"
    return build_page(
        title="Galería — Átomos Perdidos 🖼️",
        body=body, active_nav="/gallery", octeto_msg=octeto_msg,
        extra_css=GALLERY_CSS, extra_js=extra_js,
        pending_toasts=pending_toasts, include_3d=True,
    )


# ═════════════════════════════════════════════════════════════════════
#  LOGROS
# ═════════════════════════════════════════════════════════════════════

ACHIEVEMENTS_CSS = """
.ach-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin-top:14px}
.ach-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:18px;
display:flex;gap:14px;align-items:center;transition:all .25s}
.ach-emoji{font-size:2.2rem}
.ach-card.locked{opacity:.38;filter:grayscale(1)}
.ach-card.unlocked{border-color:var(--success);box-shadow:0 0 18px rgba(74,222,128,.12)}
.ach-name{font-weight:bold;font-size:.9rem}
.ach-desc{font-size:.72rem;color:var(--muted);margin-top:3px}
.ach-state{font-size:.65rem;margin-top:5px;color:var(--success);font-weight:bold}
"""


def render_achievements_page(desbloqueados: list, octeto_msg: str,
                             pending_toasts: list) -> str:
    """Vitrina de logros: desbloqueados a color, pendientes en gris."""
    cards = ""
    for logro_id, info in LOGROS.items():
        tiene = logro_id in desbloqueados
        estado = '<div class="ach-state">✔ DESBLOQUEADO</div>' if tiene else ""
        cards += f"""
<div class="ach-card {'unlocked' if tiene else 'locked'}">
  <div class="ach-emoji">{info['emoji']}</div>
  <div>
    <div class="ach-name">{info['nombre']}</div>
    <div class="ach-desc">{info['desc']}</div>
    {estado}
  </div>
</div>"""
    body = f"""
<h2>🏅 Logros</h2>
<p style="color:var(--muted);font-size:.8rem;margin-top:4px">
{len(desbloqueados)} de {len(LOGROS)} desbloqueados.</p>
<div class="ach-grid">{cards}</div>
"""
    return build_page(
        title="Logros — Átomos Perdidos 🏅",
        body=body, active_nav="/achievements", octeto_msg=octeto_msg,
        extra_css=ACHIEVEMENTS_CSS, pending_toasts=pending_toasts,
    )


# ═════════════════════════════════════════════════════════════════════
#  HISTORIA
# ═════════════════════════════════════════════════════════════════════

STORY_CSS = """
.story-card{max-width:680px;margin:20px auto;background:var(--card);border:1px solid var(--border);
border-radius:16px;padding:28px;text-align:center}
.story-title{font-size:1.7rem;font-weight:bold;background:linear-gradient(135deg,var(--warn),var(--accent));
-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:14px}
.story-text{color:var(--muted);font-size:.88rem;line-height:1.7;text-align:left;margin-bottom:18px}
.story-progress{color:var(--accent2);font-size:.8rem;margin-bottom:18px}
.story-final{background:#1a2a0a;border:1px solid #2a4a1a;border-radius:12px;padding:16px;
color:#c8e8a8;font-size:.85rem;line-height:1.6;text-align:left;margin-bottom:18px}
"""


def render_story_page(mission: dict, capitulo_actual: int, total: int,
                      terminada: bool, en_curso: bool, octeto_msg: str) -> str:
    """Portada de la misión narrativa."""
    if terminada:
        centro = f"""
<div class="story-final">{_html.escape(mission['final'])}</div>
<a class="btn btn-primary" href="/story/start">🔁 Revivir la aventura</a>
<a class="btn btn-ghost" href="/gallery">🖼️ Ver la galería</a>"""
    elif en_curso:
        centro = f"""
<div class="story-progress">📖 Progreso: capítulo {capitulo_actual + 1} de {total}</div>
<a class="btn btn-teal" href="/game/story/play">▶️ Continuar la aventura</a>
<a class="btn btn-ghost" href="/story/start">🔄 Empezar de nuevo</a>"""
    else:
        centro = '<a class="btn btn-teal" href="/story/start">🧙 Comenzar la aventura</a>'

    body = f"""
<div class="story-card">
  <div class="story-title">📖 {mission['titulo']}</div>
  <div class="story-text">{_html.escape(mission['intro'])}</div>
  <div class="story-progress">{total} capítulos · moléculas de fácil a difícil</div>
  {centro}
</div>
"""
    return build_page(
        title="Historia — Átomos Perdidos 📖",
        body=body, active_nav="/story", octeto_msg=octeto_msg,
        extra_css=STORY_CSS,
    )
