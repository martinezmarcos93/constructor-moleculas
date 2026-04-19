"""
svg_molecules.py
Genera diagramas SVG de moléculas desde Python puro.
Todas las posiciones y colores están controlados aquí.
"""

ATOM_COLORS = {
    "H":  "#FFFFFF", "O":  "#FF4444", "C":  "#444444",
    "N":  "#4477FF", "S":  "#FFCC00", "Cl": "#55CC55",
    "F":  "#88FF88", "Na": "#AA88FF", "Mg": "#66CCCC",
    "Ca": "#88AA44", "P":  "#FF8800", "Br": "#CC4400",
    "I":  "#8800CC", "Fe": "#CC6600", "Cu": "#FF8833",
    "Zn": "#8888AA",
}
ATOM_RADIUS = {"H": 14, "O": 18, "C": 18, "N": 18, "S": 20,
               "Cl": 20, "F": 16, "Na": 22, "Mg": 22, "Ca": 24,
               "P": 20, "Br": 22, "I": 22}
DEFAULT_COLOR  = "#AAAAAA"
DEFAULT_RADIUS = 18


def _atom(x, y, symbol, label_color="#FFFFFF", stroke="#000000", r=None):
    color = ATOM_COLORS.get(symbol, DEFAULT_COLOR)
    radius = r or ATOM_RADIUS.get(symbol, DEFAULT_RADIUS)
    # Texto más pequeño para símbolos de 2 letras
    fs = 11 if len(symbol) == 2 else 13
    tc = "#111111" if color in ("#FFFFFF", "#FFCC00", "#88FF88") else "#FFFFFF"
    return (
        f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" '
        f'stroke="{stroke}" stroke-width="1.5"/>\n'
        f'<text x="{x}" y="{y+4}" text-anchor="middle" font-size="{fs}" '
        f'font-weight="bold" fill="{tc}" font-family="monospace">{symbol}</text>\n'
    )


def _bond(x1, y1, x2, y2, order=1):
    lines = []
    if order == 1:
        lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                     f'stroke="#888" stroke-width="3"/>')
    elif order == 2:
        lines.append(f'<line x1="{x1}" y1="{y1-3}" x2="{x2}" y2="{y2-3}" '
                     f'stroke="#888" stroke-width="2"/>')
        lines.append(f'<line x1="{x1}" y1="{y1+3}" x2="{x2}" y2="{y2+3}" '
                     f'stroke="#888" stroke-width="2"/>')
    elif order == 3:
        lines.append(f'<line x1="{x1}" y1="{y1-5}" x2="{x2}" y2="{y2-5}" '
                     f'stroke="#888" stroke-width="2"/>')
        lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                     f'stroke="#888" stroke-width="2"/>')
        lines.append(f'<line x1="{x1}" y1="{y1+5}" x2="{x2}" y2="{y2+5}" '
                     f'stroke="#888" stroke-width="2"/>')
    return "\n".join(lines) + "\n"


def _wrap(content, w, h):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'width="{w}" height="{h}">\n'
            f'<rect width="{w}" height="{h}" rx="12" fill="#1a1a2e" opacity="0.5"/>\n'
            f'{content}</svg>')


# ─── Diagramas individuales ───────────────────

def svg_H2():
    s = _bond(40, 50, 100, 50)
    s += _atom(40, 50, "H")
    s += _atom(100, 50, "H")
    return _wrap(s, 140, 100)

def svg_O2():
    s = _bond(40, 50, 100, 50, 2)
    s += _atom(40, 50, "O")
    s += _atom(100, 50, "O")
    return _wrap(s, 140, 100)

def svg_N2():
    s = _bond(40, 50, 100, 50, 3)
    s += _atom(40, 50, "N")
    s += _atom(100, 50, "N")
    return _wrap(s, 140, 100)

def svg_F2():
    s = _bond(40, 50, 100, 50)
    s += _atom(40, 50, "F")
    s += _atom(100, 50, "F")
    return _wrap(s, 140, 100)

def svg_HCl():
    s = _bond(40, 50, 100, 50)
    s += _atom(40, 50, "H")
    s += _atom(100, 50, "Cl")
    return _wrap(s, 140, 100)

def svg_NaCl():
    s = _bond(40, 50, 100, 50)
    s += _atom(40, 50, "Na")
    s += _atom(100, 50, "Cl")
    return _wrap(s, 140, 100)

def svg_H2O():
    # Forma angular ~104.5°
    import math
    cx, cy = 90, 70
    angle = 104.5 / 2
    r = 55
    hx1 = int(cx - r * math.sin(math.radians(angle)))
    hy1 = int(cy + r * math.cos(math.radians(angle)))
    hx2 = int(cx + r * math.sin(math.radians(angle)))
    hy2 = hy1
    s  = _bond(hx1, hy1, cx, cy)
    s += _bond(hx2, hy2, cx, cy)
    s += _atom(cx, cy, "O")
    s += _atom(hx1, hy1, "H")
    s += _atom(hx2, hy2, "H")
    return _wrap(s, 180, 140)

def svg_CO2():
    s  = _bond(30, 60, 100, 60, 2)
    s += _bond(100, 60, 170, 60, 2)
    s += _atom(30, 60, "O")
    s += _atom(100, 60, "C")
    s += _atom(170, 60, "O")
    return _wrap(s, 200, 120)

def svg_NH3():
    # Pirámide trigonal
    cx, cy = 100, 45
    s  = _bond(cx, cy, 60, 95)
    s += _bond(cx, cy, 100, 100)
    s += _bond(cx, cy, 140, 95)
    s += _atom(cx, cy, "N")
    s += _atom(60, 95, "H")
    s += _atom(100, 100, "H")
    s += _atom(140, 95, "H")
    return _wrap(s, 200, 130)

def svg_CH4():
    # Tetraédrico (proyección 2D)
    cx, cy = 100, 80
    s  = _bond(cx, cy, 50, 35)
    s += _bond(cx, cy, 150, 35)
    s += _bond(cx, cy, 50, 125)
    s += _bond(cx, cy, 150, 125)
    s += _atom(cx, cy, "C")
    s += _atom(50, 35, "H")
    s += _atom(150, 35, "H")
    s += _atom(50, 125, "H")
    s += _atom(150, 125, "H")
    return _wrap(s, 200, 160)

def svg_SO2():
    import math
    cx, cy = 90, 50
    angle = 60
    r = 58
    ox1 = int(cx - r * math.cos(math.radians(angle/2)))
    oy1 = int(cy + r * math.sin(math.radians(angle/2)))
    ox2 = int(cx + r * math.cos(math.radians(angle/2)))
    oy2 = oy1
    s  = _bond(cx, cy, ox1, oy1, 2)
    s += _bond(cx, cy, ox2, oy2)
    s += _atom(cx, cy, "S")
    s += _atom(ox1, oy1, "O")
    s += _atom(ox2, oy2, "O")
    return _wrap(s, 180, 130)

def svg_H2S():
    import math
    cx, cy = 90, 65
    angle = 92 / 2
    r = 52
    hx1 = int(cx - r * math.sin(math.radians(angle)))
    hy1 = int(cy + r * math.cos(math.radians(angle)))
    hx2 = int(cx + r * math.sin(math.radians(angle)))
    hy2 = hy1
    s  = _bond(hx1, hy1, cx, cy)
    s += _bond(hx2, hy2, cx, cy)
    s += _atom(cx, cy, "S")
    s += _atom(hx1, hy1, "H")
    s += _atom(hx2, hy2, "H")
    return _wrap(s, 180, 140)

def svg_NO2():
    import math
    cx, cy = 90, 50
    angle = 57
    r = 60
    ox1 = int(cx - r * math.sin(math.radians(angle)))
    oy1 = int(cy + r * math.cos(math.radians(angle)))
    ox2 = int(cx + r * math.sin(math.radians(angle)))
    oy2 = oy1
    s  = _bond(cx, cy, ox1, oy1, 2)
    s += _bond(cx, cy, ox2, oy2)
    s += _atom(cx, cy, "N")
    s += _atom(ox1, oy1, "O")
    s += _atom(ox2, oy2, "O")
    return _wrap(s, 180, 130)

def svg_H2SO4():
    # S central, 4 O alrededor, 2 OH
    cx, cy = 130, 90
    s  = _bond(cx, cy, 60, 90, 2)   # O doble izq
    s += _bond(cx, cy, 200, 90, 2)  # O doble der
    s += _bond(cx, cy, 130, 30)     # O-H arriba
    s += _bond(cx, cy, 130, 150)    # O-H abajo
    s += _bond(130, 30, 130, 5)     # H arriba
    s += _bond(130, 150, 130, 175)  # H abajo
    s += _atom(cx, cy, "S")
    s += _atom(60, 90, "O")
    s += _atom(200, 90, "O")
    s += _atom(130, 30, "O")
    s += _atom(130, 150, "O")
    s += _atom(130, 5, "H")
    s += _atom(130, 175, "H")
    return _wrap(s, 260, 195)

def svg_HNO3():
    cx, cy = 110, 80
    s  = _bond(cx, cy, 50, 80, 2)   # O doble
    s += _bond(cx, cy, 155, 45)     # O-H
    s += _bond(cx, cy, 155, 115)    # O
    s += _bond(155, 45, 195, 20)    # H
    s += _atom(cx, cy, "N")
    s += _atom(50, 80, "O")
    s += _atom(155, 45, "O")
    s += _atom(155, 115, "O")
    s += _atom(195, 20, "H")
    return _wrap(s, 220, 155)

def svg_C2H5OH():
    # CH3-CH2-OH lineal simplificado
    s  = _bond(30, 80, 80, 80)
    s += _bond(80, 80, 130, 80)
    s += _bond(130, 80, 180, 80)
    # H del CH3
    s += _bond(30, 80, 10, 55)
    s += _bond(30, 80, 10, 105)
    # H del CH2
    s += _bond(80, 80, 80, 45)
    s += _bond(80, 80, 80, 115)
    # H del OH
    s += _bond(180, 80, 210, 55)
    s += _atom(30, 80, "C")
    s += _atom(80, 80, "C")
    s += _atom(130, 80, "O")
    s += _atom(180, 80, "H")
    s += _atom(10, 55, "H")
    s += _atom(10, 105, "H")
    s += _atom(80, 45, "H")
    s += _atom(80, 115, "H")
    s += _atom(210, 55, "H")
    return _wrap(s, 240, 160)

def svg_CH3COOH():
    s  = _bond(30, 80, 90, 80)
    s += _bond(90, 80, 150, 80)
    s += _bond(150, 80, 210, 55, 2)
    s += _bond(150, 80, 210, 105)
    s += _bond(210, 105, 240, 80)
    # H del CH3
    s += _bond(30, 80, 10, 55)
    s += _bond(30, 80, 10, 105)
    s += _bond(30, 80, 30, 45)
    s += _atom(30, 80, "C")
    s += _atom(150, 80, "C")
    s += _atom(210, 55, "O")
    s += _atom(210, 105, "O")
    s += _atom(240, 80, "H")
    s += _atom(10, 55, "H")
    s += _atom(10, 105, "H")
    s += _atom(30, 45, "H")
    return _wrap(s, 270, 160)

def svg_NaOH():
    s  = _bond(40, 60, 100, 60)
    s += _bond(100, 60, 160, 60)
    s += _atom(40, 60, "Na")
    s += _atom(100, 60, "O")
    s += _atom(160, 60, "H")
    return _wrap(s, 200, 120)

def svg_MgCl2():
    s  = _bond(40, 60, 110, 60)
    s += _bond(110, 60, 180, 60)
    s += _atom(40, 60, "Cl")
    s += _atom(110, 60, "Mg")
    s += _atom(180, 60, "Cl")
    return _wrap(s, 220, 120)

def svg_CaCO3():
    cx, cy = 120, 80
    s  = _bond(cx, cy, 60, 80, 2)
    s += _bond(cx, cy, 165, 35)
    s += _bond(cx, cy, 165, 125)
    s += _bond(165, 35, 210, 35)
    s += _atom(cx, cy, "C")
    s += _atom(60, 80, "O")
    s += _atom(165, 35, "O")
    s += _atom(165, 125, "O")
    s += _atom(210, 35, "Ca")
    return _wrap(s, 250, 165)


# ─── Registro ────────────────────────────────

SVG_REGISTRY = {
    "H2":       svg_H2,
    "O2":       svg_O2,
    "N2":       svg_N2,
    "F2":       svg_F2,
    "HCl":      svg_HCl,
    "NaCl":     svg_NaCl,
    "H2O":      svg_H2O,
    "CO2":      svg_CO2,
    "NH3":      svg_NH3,
    "CH4":      svg_CH4,
    "SO2":      svg_SO2,
    "H2S":      svg_H2S,
    "NO2":      svg_NO2,
    "H2SO4":    svg_H2SO4,
    "HNO3":     svg_HNO3,
    "C2H5OH":   svg_C2H5OH,
    "CH3COOH":  svg_CH3COOH,
    "NaOH":     svg_NaOH,
    "MgCl2":    svg_MgCl2,
    "CaCO3":    svg_CaCO3,
}


def get_svg(key: str) -> str:
    fn = SVG_REGISTRY.get(key)
    if fn:
        return fn()
    return _wrap(f'<text x="50" y="50" fill="#aaa" font-size="12">Sin imagen</text>', 120, 80)
