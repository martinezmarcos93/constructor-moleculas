"""
svg_molecules.py  ─  Átomos Perdidos v1.1
Diagramas SVG generados 100 % desde Python.
Cubre las 63 moléculas de la base de datos ampliada.
Donde no hay SVG dedicado se genera automáticamente un diagrama lineal genérico.
"""
import math

# ── Paleta de átomos ─────────────────────────────
ATOM_COLORS = {
    "H": "#EEEEEE", "He": "#D9FFFF",
    "Li": "#CC80FF", "Be": "#C2FF00",
    "B": "#FFB5B5",  "C": "#404040",  "N": "#3050F8",  "O": "#FF2020",
    "F": "#90E050",  "Ne": "#B3E3F5",
    "Na": "#AB5CF2", "Mg": "#8AFF00",
    "Al": "#BFA6A6", "Si": "#F0C8A0", "P": "#FF8000",  "S": "#FFFF30",
    "Cl": "#1FF01F", "Ar": "#80D1E3",
    "K": "#8F40D4",  "Ca": "#3DFF00",
    "Fe": "#E06633", "Cu": "#C88033", "Zn": "#7D80B0",
    "Br": "#A62929", "I": "#940094",
}
ATOM_RADIUS = {
    "H": 13, "C": 17, "N": 17, "O": 17, "F": 15,
    "S": 19, "P": 19, "Si": 19, "B": 17,
    "Cl": 19, "Br": 21, "I": 21,
    "Na": 21, "K": 23, "Li": 17, "Mg": 20, "Ca": 23,
    "Fe": 20, "Cu": 20, "Zn": 19,
}
DEFAULT_COLOR  = "#AAAAAA"
DEFAULT_RADIUS = 17


# ── Primitivas SVG ───────────────────────────────

def _atom(x, y, symbol, r=None):
    color  = ATOM_COLORS.get(symbol, DEFAULT_COLOR)
    radius = r or ATOM_RADIUS.get(symbol, DEFAULT_RADIUS)
    fs     = 10 if len(symbol) == 2 else 12
    # Contraste texto
    bright = color in ("#EEEEEE","#FFFF30","#90E050","#C2FF00","#8AFF00","#3DFF00","#F0C8A0","#FFB5B5","#FF8000","#B3E3F5","#80D1E3","#D9FFFF","#FFFFFF")
    tc = "#111111" if bright else "#FFFFFF"
    return (
        f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" '
        f'stroke="rgba(0,0,0,0.4)" stroke-width="1.5"/>\n'
        f'<text x="{x}" y="{y+4}" text-anchor="middle" '
        f'font-size="{fs}" font-weight="bold" fill="{tc}" '
        f'font-family="monospace">{symbol}</text>\n'
    )

def _bond(x1, y1, x2, y2, order=1, color="#777777"):
    out = ""
    if order == 1:
        out = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2.5" stroke-linecap="round"/>\n'
    elif order == 2:
        dx = y2 - y1; dy = x1 - x2
        norm = math.hypot(dx, dy) or 1
        ox = dx / norm * 3; oy = dy / norm * 3
        for sg in (-1, 1):
            x1o, y1o = x1 + sg*ox, y1 + sg*oy
            x2o, y2o = x2 + sg*ox, y2 + sg*oy
            out += f'<line x1="{x1o:.1f}" y1="{y1o:.1f}" x2="{x2o:.1f}" y2="{y2o:.1f}" stroke="{color}" stroke-width="2" stroke-linecap="round"/>\n'
    elif order == 3:
        dx = y2 - y1; dy = x1 - x2
        norm = math.hypot(dx, dy) or 1
        ox = dx / norm * 4; oy = dy / norm * 4
        for sg in (-1, 0, 1):
            x1o, y1o = x1 + sg*ox, y1 + sg*oy
            x2o, y2o = x2 + sg*ox, y2 + sg*oy
            out += f'<line x1="{x1o:.1f}" y1="{y1o:.1f}" x2="{x2o:.1f}" y2="{y2o:.1f}" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>\n'
    return out

def _wrap(content, w, h, bg="#0d0d22"):
    return (
        f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
        f'width="{w}" height="{h}" style="border-radius:10px">\n'
        f'<rect width="{w}" height="{h}" rx="10" fill="{bg}"/>\n'
        f'{content}</svg>'
    )

def _label(x, y, text, color="#666688", size=9):
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{color}" font-family="monospace">{text}</text>\n'


# ── Diagramas dedicados ──────────────────────────

# ─ Diatómicas simples ─
def _diatomic(sym1, sym2, order=1):
    s = _bond(38, 50, 98, 50, order)
    s += _atom(38, 50, sym1)
    s += _atom(98, 50, sym2)
    return _wrap(s, 136, 100)

def svg_H2():   return _diatomic("H", "H")
def svg_O2():   return _diatomic("O", "O", 2)
def svg_N2():   return _diatomic("N", "N", 3)
def svg_F2():   return _diatomic("F", "F")
def svg_Cl2():  return _diatomic("Cl","Cl")
def svg_Br2():  return _diatomic("Br","Br")
def svg_I2():   return _diatomic("I", "I")
def svg_HCl():  return _diatomic("H", "Cl")
def svg_HF():   return _diatomic("H", "F")
def svg_HBr():  return _diatomic("H", "Br")
def svg_HI():   return _diatomic("H", "I")
def svg_CO():   return _diatomic("C", "O", 3)
def svg_NO():   return _diatomic("N", "O", 2)
def svg_NaCl(): return _diatomic("Na","Cl")
def svg_LiH():  return _diatomic("Li","H")
def svg_KBr():  return _diatomic("K", "Br")
def svg_MgO():  return _diatomic("Mg","O")
def svg_CaO():  return _diatomic("Ca","O")

# ─ Triatómicas lineales ─
def _trilinear(l, c, r, bl=1, br=1):
    s = _bond(28, 55, 100, 55, bl)
    s += _bond(100, 55, 172, 55, br)
    s += _atom(28, 55, l)
    s += _atom(100, 55, c)
    s += _atom(172, 55, r)
    return _wrap(s, 200, 110)

def svg_CO2():  return _trilinear("O","C","O",2,2)
def svg_SO3():  # SO3 trigonal plano
    cx,cy = 100,60
    s  = _bond(cx,cy, 45,105,2)
    s += _bond(cx,cy,155,105)
    s += _bond(cx,cy,100, 10,2)
    s += _atom(cx,cy,"S")
    s += _atom(45,105,"O"); s += _atom(155,105,"O"); s += _atom(100,10,"O")
    return _wrap(s,200,130)

def svg_N2O():   # N=N=O lineal
    s  = _bond(30,55,100,55,2)
    s  += _bond(100,55,170,55,2)
    s += _atom(30,55,"N"); s += _atom(100,55,"N"); s += _atom(170,55,"O")
    return _wrap(s,200,110)

def svg_Na2O():
    s  = _bond(30,55, 95,55)
    s += _bond(95,55,160,55)
    s += _atom(30,55,"Na"); s += _atom(95,55,"O"); s += _atom(160,55,"Na")
    return _wrap(s,190,110)

def svg_SiO2():
    return _trilinear("O","Si","O",2,2)

# ─ Angulares ─
def _angular(sym_c, sym_l, sym_r, angle_deg=104.5, r=55, order_l=1, order_r=1):
    cx,cy = 100,70
    ha = math.radians(angle_deg/2)
    lx = int(cx - r*math.sin(ha)); ly = int(cy + r*math.cos(ha))
    rx = int(cx + r*math.sin(ha)); ry = ly
    s  = _bond(lx,ly,cx,cy,order_l)
    s += _bond(rx,ry,cx,cy,order_r)
    s += _atom(cx,cy,sym_c)
    s += _atom(lx,ly,sym_l)
    s += _atom(rx,ry,sym_r)
    return _wrap(s,200,140)

def svg_H2O():  return _angular("O","H","H",104.5)
def svg_SO2():  return _angular("S","O","O",119,58,2,1)
def svg_H2S():  return _angular("S","H","H",92)
def svg_NO2():  return _angular("N","O","O",134,58,2,1)
def svg_H2O2():
    # H-O-O-H con puente
    s  = _bond(20,70, 80,55)
    s += _bond(80,55,140,55)
    s += _bond(140,55,200,70)
    s += _atom(20,70,"H"); s += _atom(80,55,"O")
    s += _atom(140,55,"O"); s += _atom(200,70,"H")
    return _wrap(s,220,115)

# ─ Pirámide trigonal ─
def _trigpyramid(sym_c, sym_h, angle_out=100, r_out=55):
    cx,cy = 100,42
    angles = [210, 330, 90]
    pos = [(int(cx+r_out*math.cos(math.radians(a))),
            int(cy+r_out*math.sin(math.radians(a)))) for a in angles]
    s = ""
    for px,py in pos:
        s += _bond(cx,cy,px,py)
    s += _atom(cx,cy,sym_c)
    for px,py in pos:
        s += _atom(px,py,sym_h)
    return _wrap(s,200,160)

def svg_NH3():  return _trigpyramid("N","H")
def svg_PH3():  return _trigpyramid("P","H")

# ─ Tetraédrico ─
def _tetrahedral(sym_c, sym_h):
    cx,cy = 100,80
    corners = [(50,35),(150,35),(50,125),(150,125)]
    s = ""
    for px,py in corners:
        s += _bond(cx,cy,px,py)
    s += _atom(cx,cy,sym_c)
    for px,py in corners:
        s += _atom(px,py,sym_h)
    return _wrap(s,200,165)

def svg_CH4():  return _tetrahedral("C","H")
def svg_SiH4(): return _tetrahedral("Si","H")
def svg_CCl4(): return _tetrahedral("C","Cl")

def svg_BH3():
    cx,cy = 100,80
    pts = [(100,25),(55,118),(145,118)]
    s = ""
    for px,py in pts:
        s += _bond(cx,cy,px,py)
    s += _atom(cx,cy,"B")
    for px,py in pts:
        s += _atom(px,py,"H")
    return _wrap(s,200,150)

# ─ Octaédrico SF6 ─
def svg_SF6():
    cx,cy = 110,110
    pts = [(110,50),(110,170),(50,110),(170,110),(65,65),(155,155)]
    s = ""
    for px,py in pts:
        s += _bond(cx,cy,px,py)
    s += _atom(cx,cy,"S")
    for px,py in pts:
        s += _atom(px,py,"F")
    return _wrap(s,220,220)

def svg_PCl3():
    cx,cy = 100,42
    pts = [(40,120),(100,130),(160,120)]
    s = ""
    for px,py in pts:
        s += _bond(cx,cy,px,py)
    s += _atom(cx,cy,"P")
    for px,py in pts:
        s += _atom(px,py,"Cl")
    return _wrap(s,200,165)

# ─ Lineales C₂ ─
def svg_C2H2():
    s  = _bond(30,55, 80,55)
    s += _bond(80,55,130,55,3)
    s += _bond(130,55,180,55)
    s += _atom(30,55,"H"); s += _atom(80,55,"C")
    s += _atom(130,55,"C"); s += _atom(180,55,"H")
    return _wrap(s,210,110)

def svg_C2H4():   # H₂C=CH₂ plano
    s  = _bond(50,80,110,80,2)
    s += _bond(30,45, 50,80); s += _bond(30,115,50,80)
    s += _bond(110,80,130,45); s += _bond(110,80,130,115)
    s += _atom(50,80,"C"); s += _atom(110,80,"C")
    s += _atom(30,45,"H"); s += _atom(30,115,"H")
    s += _atom(130,45,"H"); s += _atom(130,115,"H")
    return _wrap(s,160,160)

def svg_C2H6():   # etano en zigzag
    s  = _bond(50,80,120,80)
    s += _bond(30,45,50,80); s += _bond(30,115,50,80); s += _bond(50,80,50,45)
    s += _bond(120,80,140,45); s += _bond(120,80,140,115); s += _bond(120,80,120,45)
    s += _atom(50,80,"C"); s += _atom(120,80,"C")
    for pos in [(30,45),(30,115),(50,45),(140,45),(140,115),(120,45)]:
        s += _atom(*pos,"H")
    return _wrap(s,170,160)

def svg_N2H4():
    s  = _bond(70,80,140,80)
    s += _bond(50,45,70,80); s += _bond(50,115,70,80)
    s += _bond(140,80,160,45); s += _bond(140,80,160,115)
    s += _atom(70,80,"N"); s += _atom(140,80,"N")
    s += _atom(50,45,"H"); s += _atom(50,115,"H")
    s += _atom(160,45,"H"); s += _atom(160,115,"H")
    return _wrap(s,210,160)

# ─ CH₃OH metanol ─
def svg_CH3OH():
    s  = _bond(50,80,120,80); s += _bond(120,80,175,80)
    s += _bond(30,45,50,80); s += _bond(30,115,50,80); s += _bond(50,80,50,45)
    s += _bond(175,80,205,55)
    s += _atom(50,80,"C"); s += _atom(120,80,"O")
    s += _atom(175,80,"H"); s += _atom(205,55,"H")
    s += _atom(30,45,"H"); s += _atom(30,115,"H"); s += _atom(50,45,"H")
    return _wrap(s,225,160)

# ─ Formaldehído HCHO ─
def svg_HCHO():
    s  = _bond(50,80,120,80); s += _bond(120,80,180,80,2)
    s += _bond(50,80,25,55); s += _bond(50,80,25,105)
    s += _atom(50,80,"C"); s += _atom(180,80,"O")
    s += _atom(25,55,"H"); s += _atom(25,105,"H")
    return _wrap(s,210,160)

# ─ H₂SO₄ ─
def svg_H2SO4():
    cx,cy = 130,95
    s  = _bond(cx,cy,65,95,2); s += _bond(cx,cy,195,95,2)
    s += _bond(cx,cy,130,35);  s += _bond(cx,cy,130,155)
    s += _bond(130,35,130,8);  s += _bond(130,155,130,182)
    s += _atom(cx,cy,"S"); s += _atom(65,95,"O"); s += _atom(195,95,"O")
    s += _atom(130,35,"O"); s += _atom(130,155,"O")
    s += _atom(130,8,"H"); s += _atom(130,182,"H")
    return _wrap(s,260,200)

# ─ HNO₃ ─
def svg_HNO3():
    cx,cy = 110,80
    s  = _bond(cx,cy,50,80,2); s += _bond(cx,cy,155,45); s += _bond(cx,cy,155,115)
    s += _bond(155,45,195,20)
    s += _atom(cx,cy,"N"); s += _atom(50,80,"O")
    s += _atom(155,45,"O"); s += _atom(155,115,"O"); s += _atom(195,20,"H")
    return _wrap(s,220,155)

# ─ H₃PO₄ ─
def svg_H3PO4():
    cx,cy = 120,95
    s  = _bond(cx,cy,65,95,2)
    s += _bond(cx,cy,120,35); s += _bond(cx,cy,175,55); s += _bond(cx,cy,175,135)
    s += _bond(120,35,120,8); s += _bond(175,55,205,30); s += _bond(175,135,205,155)
    s += _atom(cx,cy,"P"); s += _atom(65,95,"O")
    s += _atom(120,35,"O"); s += _atom(175,55,"O"); s += _atom(175,135,"O")
    s += _atom(120,8,"H"); s += _atom(205,30,"H"); s += _atom(205,155,"H")
    return _wrap(s,240,180)

# ─ NaOH ─
def svg_NaOH():
    s  = _bond(38,60,100,60); s += _bond(100,60,162,60)
    s += _atom(38,60,"Na"); s += _atom(100,60,"O"); s += _atom(162,60,"H")
    return _wrap(s,200,120)

# ─ MgCl₂ ─
def svg_MgCl2():
    s  = _bond(38,60,110,60); s += _bond(110,60,182,60)
    s += _atom(38,60,"Cl"); s += _atom(110,60,"Mg"); s += _atom(182,60,"Cl")
    return _wrap(s,220,120)

# ─ CaCO₃ ─
def svg_CaCO3():
    cx,cy = 120,80
    s  = _bond(cx,cy,60,80,2); s += _bond(cx,cy,165,35); s += _bond(cx,cy,165,125)
    s += _bond(165,35,210,35)
    s += _atom(cx,cy,"C"); s += _atom(60,80,"O")
    s += _atom(165,35,"O"); s += _atom(165,125,"O"); s += _atom(210,35,"Ca")
    return _wrap(s,250,165)

# ─ P₄ tetraédrico ─
def svg_P4():
    pts = [(100,25),(40,130),(160,130),(100,95)]
    bonds = [(0,1),(0,2),(1,2),(0,3),(1,3),(2,3)]
    s = ""
    for a,b in bonds:
        s += _bond(*pts[a],*pts[b])
    for px,py in pts:
        s += _atom(px,py,"P")
    return _wrap(s,200,170)

# ─ Cadenas carbono ─
def _chain(symbols, bonds_override=None):
    """Genera una cadena lineal en zigzag con H implícitos como etiqueta."""
    n = len(symbols)
    W = 50 + n * 60
    H = 140
    cx = [50 + i*60 for i in range(n)]
    cy = [70 - (i%2)*20 for i in range(n)]
    s = ""
    for i in range(n-1):
        order = bonds_override[i] if bonds_override else 1
        s += _bond(cx[i],cy[i],cx[i+1],cy[i+1],order)
    for i,sym in enumerate(symbols):
        s += _atom(cx[i],cy[i],sym)
    return _wrap(s,W,H)

def svg_C2H5OH():
    s  = _bond(40,80,100,80); s += _bond(100,80,160,80); s += _bond(160,80,210,80)
    s += _bond(25,50,40,80); s += _bond(25,110,40,80)
    s += _bond(100,80,100,45); s += _bond(100,80,100,115)
    s += _bond(210,80,230,55)
    s += _atom(40,80,"C"); s += _atom(100,80,"C"); s += _atom(160,80,"O"); s += _atom(210,80,"H")
    s += _atom(25,50,"H"); s += _atom(25,110,"H")
    s += _atom(100,45,"H"); s += _atom(100,115,"H"); s += _atom(230,55,"H")
    return _wrap(s,260,170)

def svg_CH3COOH():
    s  = _bond(35,80, 95,80); s += _bond(95,80,155,80)
    s += _bond(155,80,205,55,2); s += _bond(155,80,205,105); s += _bond(205,105,235,80)
    s += _bond(15,50,35,80); s += _bond(15,110,35,80); s += _bond(35,80,35,45)
    s += _atom(35,80,"C"); s += _atom(95,80,"C")
    s += _atom(205,55,"O"); s += _atom(205,105,"O"); s += _atom(235,80,"H")
    s += _atom(15,50,"H"); s += _atom(15,110,"H"); s += _atom(35,45,"H")
    return _wrap(s,265,165)

def svg_HCOOH():
    s  = _bond(30,80,100,80); s += _bond(100,80,155,55,2); s += _bond(100,80,155,105); s += _bond(155,105,185,80)
    s += _atom(30,80,"H"); s += _atom(100,80,"C"); s += _atom(155,55,"O"); s += _atom(155,105,"O"); s += _atom(185,80,"H")
    return _wrap(s,215,155)

def svg_CH3NH2():
    s  = _bond(50,80,120,80); s += _bond(120,80,175,80)
    s += _bond(30,50,50,80); s += _bond(30,110,50,80); s += _bond(50,80,50,45)
    s += _bond(175,80,200,55); s += _bond(175,80,200,105)
    s += _atom(50,80,"C"); s += _atom(120,80,"N")
    s += _atom(30,50,"H"); s += _atom(30,110,"H"); s += _atom(50,45,"H")
    s += _atom(175,80,"H"); s += _atom(200,55,"H"); s += _atom(200,105,"H")
    return _wrap(s,230,160)

def svg_C3H8():
    s  = _bond(40,80,100,65); s += _bond(100,65,160,80); s += _bond(160,80,220,65)
    for cx,cy in [(40,80),(100,65),(160,80),(220,65)]:
        pass
    # Hidrógenos simplificados: solo etiqueta
    s  = _bond(40,80,100,65); s += _bond(100,65,160,80)
    s += _bond(20,50,40,80); s += _bond(20,110,40,80); s += _bond(40,80,40,45)
    s += _bond(100,65,80,35); s += _bond(100,65,120,35)
    s += _bond(160,80,140,110); s += _bond(160,80,180,110)
    s += _bond(160,80,200,60)
    s += _atom(40,80,"C"); s += _atom(100,65,"C"); s += _atom(160,80,"C")
    for pos in [(20,50),(20,110),(40,45),(80,35),(120,35),(140,110),(180,110),(200,60)]:
        s += _atom(*pos,"H")
    return _wrap(s,230,145)

def svg_C4H10():
    # Cadena de 4 C en zigzag
    cx_list = [35, 95, 155, 215]
    cy_list = [85, 65, 85, 65]
    s = ""
    for i in range(3):
        s += _bond(cx_list[i],cy_list[i],cx_list[i+1],cy_list[i+1])
    for cx,cy in zip(cx_list,cy_list):
        s += _atom(cx,cy,"C")
    # H simplificados con etiqueta
    s += _label(35,115,"H₃",  "#aaa",10)
    s += _label(95,38, "H₂",  "#aaa",10)
    s += _label(155,115,"H₂", "#aaa",10)
    s += _label(215,38,"H₃",  "#aaa",10)
    return _wrap(s,255,135)

def svg_C8H18():
    # Representación abreviada
    s  = '<text x="110" y="60" text-anchor="middle" font-size="22" font-weight="bold" fill="#b0c4ff" font-family="monospace">C₈H₁₈</text>\n'
    s += '<text x="110" y="82" text-anchor="middle" font-size="10" fill="#6666aa" font-family="monospace">n-octano</text>\n'
    # dibuja cadena lineal simplificada
    for i in range(8):
        x = 15 + i*25
        y = 105 + (i%2)*15
        if i > 0:
            s += f'<line x1="{15+(i-1)*25}" y1="{105+((i-1)%2)*15}" x2="{x}" y2="{y}" stroke="#555" stroke-width="2"/>\n'
        s += f'<circle cx="{x}" cy="{y}" r="8" fill="#404040" stroke="#666" stroke-width="1"/>\n'
        s += f'<text x="{x}" y="{y+3}" text-anchor="middle" font-size="7" fill="#ddd" font-family="monospace">C</text>\n'
    return _wrap(s,220,145)

# ─ Anillo bencénico ─
def _benzene_ring(cx,cy,r,symbols=None,extra=""):
    """Hexágono aromático con círculo interior."""
    angles = [90,30,-30,-90,-150,150]  # grados, desde arriba
    pts = [(int(cx+r*math.cos(math.radians(a))),
            int(cy-r*math.sin(math.radians(a)))) for a in angles]
    s = ""
    # Lados del hexágono
    for i in range(6):
        s += _bond(*pts[i],*pts[(i+1)%6])
    # Círculo interior (aromaticidad)
    s += f'<circle cx="{cx}" cy="{cy}" r="{int(r*0.55)}" fill="none" stroke="#555" stroke-width="1.2" stroke-dasharray="3,2"/>\n'
    # Átomos C en cada vértice (pequeño)
    for px,py in pts:
        s += f'<circle cx="{px}" cy="{py}" r="9" fill="{ATOM_COLORS["C"]}" stroke="rgba(0,0,0,0.3)" stroke-width="1"/>\n'
        s += f'<text x="{px}" y="{py+3}" text-anchor="middle" font-size="8" font-weight="bold" fill="#fff" font-family="monospace">C</text>\n'
    if extra:
        s += extra
    return s, pts

def svg_C6H6():
    cx,cy,r = 100,100,55
    s, pts = _benzene_ring(cx,cy,r)
    # H externos
    for i,(px,py) in enumerate(pts):
        ang = math.radians([90,30,-30,-90,-150,150][i])
        hx = int(px + 26*math.cos(math.radians([90,30,-30,-90,-150,150][i])*0 + [90,30,-30,-90,-150,150][i]))
        hy = int(py - 26*math.sin(math.radians([90,30,-30,-90,-150,150][i])))
        hx = int(cx + (r+28)*math.cos(math.radians([90,30,-30,-90,-150,150][i])))
        hy = int(cy - (r+28)*math.sin(math.radians([90,30,-30,-90,-150,150][i])))
        s += _bond(px,py,hx,hy)
        s += _atom(hx,hy,"H")
    return _wrap(s,200,200)

def svg_C6H5OH():
    cx,cy,r = 95,105,50
    s, pts = _benzene_ring(cx,cy,r)
    # OH en posición 0 (arriba)
    ohx,ohy = int(cx + (r+30)*math.cos(math.radians(90))), int(cy - (r+30)*math.sin(math.radians(90)))
    hx2,hy2 = ohx+22, ohy-10
    s += _bond(*pts[0],ohx,ohy); s += _bond(ohx,ohy,hx2,hy2)
    s += _atom(ohx,ohy,"O"); s += _atom(hx2,hy2,"H")
    for i,ang in enumerate([30,-30,-90,-150,150]):
        px = int(cx + (r+24)*math.cos(math.radians(ang)))
        py = int(cy - (r+24)*math.sin(math.radians(ang)))
        s += _bond(*pts[i+1],px,py); s += _atom(px,py,"H")
    return _wrap(s,220,215)

def svg_C6H5CH3():
    cx,cy,r = 90,110,50
    s, pts = _benzene_ring(cx,cy,r)
    # CH₃ en posición 0
    chx,chy = int(cx+(r+35)*math.cos(math.radians(90))), int(cy-(r+35)*math.sin(math.radians(90)))
    s += _bond(*pts[0],chx,chy); s += _atom(chx,chy,"C")
    s += _label(chx,chy+22,"H₃","#aaa",9)
    for i,ang in enumerate([30,-30,-90,-150,150]):
        px = int(cx+(r+24)*math.cos(math.radians(ang)))
        py = int(cy-(r+24)*math.sin(math.radians(ang)))
        s += _bond(*pts[i+1],px,py); s += _atom(px,py,"H")
    return _wrap(s,215,215)

def svg_C6H5NH2():
    cx,cy,r = 95,110,50
    s, pts = _benzene_ring(cx,cy,r)
    nx,ny = int(cx+(r+30)*math.cos(math.radians(90))), int(cy-(r+30)*math.sin(math.radians(90)))
    h1x,h1y = nx-18,ny-12;  h2x,h2y = nx+18,ny-12
    s += _bond(*pts[0],nx,ny); s += _bond(nx,ny,h1x,h1y); s += _bond(nx,ny,h2x,h2y)
    s += _atom(nx,ny,"N"); s += _atom(h1x,h1y,"H"); s += _atom(h2x,h2y,"H")
    for i,ang in enumerate([30,-30,-90,-150,150]):
        px=int(cx+(r+24)*math.cos(math.radians(ang))); py=int(cy-(r+24)*math.sin(math.radians(ang)))
        s += _bond(*pts[i+1],px,py); s += _atom(px,py,"H")
    return _wrap(s,215,215)

def svg_C6H5NO2():
    cx,cy,r = 95,115,50
    s, pts = _benzene_ring(cx,cy,r)
    nx,ny = int(cx+(r+30)*math.cos(math.radians(90))), int(cy-(r+30)*math.sin(math.radians(90)))
    o1x,o1y = nx-22,ny-15;  o2x,o2y = nx+22,ny-15
    s += _bond(*pts[0],nx,ny); s += _bond(nx,ny,o1x,o1y,2); s += _bond(nx,ny,o2x,o2y)
    s += _atom(nx,ny,"N"); s += _atom(o1x,o1y,"O"); s += _atom(o2x,o2y,"O")
    for i,ang in enumerate([30,-30,-90,-150,150]):
        px=int(cx+(r+24)*math.cos(math.radians(ang))); py=int(cy-(r+24)*math.sin(math.radians(ang)))
        s += _bond(*pts[i+1],px,py); s += _atom(px,py,"H")
    return _wrap(s,215,215)

def svg_CH3COCH3():
    # CH₃-C(=O)-CH₃
    s  = _bond(30,90, 90,90);  s += _bond(90,90,150,90,1)
    s += _bond(150,90,210,90); s += _bond(90,90,90,35,2)
    s += _atom(30,90,"C"); s += _atom(90,90,"C"); s += _atom(150,90,"C"); s += _atom(210,90,"C")
    s += _atom(90,35,"O")
    s += _label(30,120, "H₃","#aaa",9); s += _label(210,120,"H₃","#aaa",9)
    s += _label(150,120,"H₂","#aaa",9)
    return _wrap(s,245,150)

def svg_NH4NO3():
    # NH₄⁺ — NO₃⁻ simplificado
    s  = '<text x="105" y="55" text-anchor="middle" font-size="11" fill="#aaa" font-family="monospace">NH₄⁺  ·  NO₃⁻</text>\n'
    # NH₄⁺
    cx,cy = 60,100
    for ang in [90,0,180,270]:
        hx=int(cx+38*math.cos(math.radians(ang))); hy=int(cy-38*math.sin(math.radians(ang)))
        s += _bond(cx,cy,hx,hy); s += _atom(hx,hy,"H")
    s += _atom(cx,cy,"N")
    # NO₃⁻
    cx2,cy2=155,100
    s += _bond(cx2,cy2,cx2-35,cy2+35,2); s += _bond(cx2,cy2,cx2+35,cy2+35); s += _bond(cx2,cy2,cx2,cy2-45)
    s += _atom(cx2,cy2,"N"); s += _atom(cx2-35,cy2+35,"O"); s += _atom(cx2+35,cy2+35,"O"); s += _atom(cx2,cy2-45,"O")
    return _wrap(s,215,175)

def svg_C2H5OC2H5():
    # Et-O-Et simplificado
    s  = _bond(30,80,90,80); s += _bond(90,80,145,80); s += _bond(145,80,205,80)
    s += _atom(30,80,"C"); s += _atom(90,80,"C"); s += _atom(145,80,"O"); s += _atom(205,80,"C")
    s += _label(30,108,"H₃","#aaa",9); s += _label(90,108,"H₂","#aaa",9)
    s += _label(205,108,"H₂","#aaa",9)
    # 2do etilo
    s += _bond(205,80,250,80); s += _atom(250,80,"C"); s += _label(250,108,"H₃","#aaa",9)
    return _wrap(s,285,135)


# ── Registro completo ────────────────────────────

SVG_REGISTRY = {
    # Diatómicas
    "H2": svg_H2,  "O2": svg_O2,  "N2": svg_N2,
    "F2": svg_F2,  "Cl2":svg_Cl2, "Br2":svg_Br2, "I2": svg_I2,
    "HCl":svg_HCl, "HF": svg_HF,  "HBr":svg_HBr, "HI": svg_HI,
    "CO": svg_CO,  "NO": svg_NO,
    "NaCl":svg_NaCl,"LiH":svg_LiH,"KBr":svg_KBr,
    "MgO":svg_MgO, "CaO":svg_CaO,
    # Triatómicas / simples
    "H2O":svg_H2O, "CO2":svg_CO2, "SO2":svg_SO2,
    "SO3":svg_SO3, "N2O":svg_N2O, "NO2":svg_NO2,
    "H2S":svg_H2S, "H2O2":svg_H2O2,
    "Na2O":svg_Na2O,"SiO2":svg_SiO2,
    # Pirámide / tetraédrico
    "NH3":svg_NH3, "PH3":svg_PH3,
    "CH4":svg_CH4, "SiH4":svg_SiH4,"CCl4":svg_CCl4,
    "BH3":svg_BH3, "SF6":svg_SF6,  "PCl3":svg_PCl3,
    # Enlace múltiple
    "C2H2":svg_C2H2,"C2H4":svg_C2H4,"C2H6":svg_C2H6,
    "N2H4":svg_N2H4,
    # Función oxigenada
    "CH3OH":svg_CH3OH, "HCHO":svg_HCHO,
    # Ácidos inorgánicos
    "H2SO4":svg_H2SO4,"HNO3":svg_HNO3,"H3PO4":svg_H3PO4,
    # Bases / sales
    "NaOH":svg_NaOH,"MgCl2":svg_MgCl2,"CaCO3":svg_CaCO3,
    # P₄
    "P4":svg_P4,
    # Cadenas
    "C3H8":svg_C3H8,"C4H10":svg_C4H10,"C8H18":svg_C8H18,
    "C2H5OH":svg_C2H5OH,"CH3COOH":svg_CH3COOH,
    "HCOOH":svg_HCOOH,"CH3NH2":svg_CH3NH2,
    "CH3COCH3":svg_CH3COCH3,"NH4NO3":svg_NH4NO3,
    "C2H5OC2H5":svg_C2H5OC2H5,
    # Aromáticos
    "C6H6":svg_C6H6,"C6H5OH":svg_C6H5OH,
    "C6H5CH3":svg_C6H5CH3,"C6H5NH2":svg_C6H5NH2,
    "C6H5NO2":svg_C6H5NO2,
}


def get_svg(key: str) -> str:
    """Devuelve el SVG para la clave dada, o un placeholder genérico."""
    fn = SVG_REGISTRY.get(key)
    if fn:
        try:
            return fn()
        except Exception:
            pass
    # Fallback: badge con fórmula
    return _wrap(
        f'<text x="70" y="50" text-anchor="middle" font-size="18" '
        f'font-weight="bold" fill="#7c6af7" font-family="monospace">{key}</text>'
        f'<text x="70" y="68" text-anchor="middle" font-size="9" '
        f'fill="#555577" font-family="monospace">sin diagrama</text>',
        140, 90
    )
