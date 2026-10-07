"""
molecule_3d.py  ─  Átomos Perdidos v2
Coordenadas 3D aproximadas para el visor 3Dmol.js, calculadas en Python
con geometría VSEPR básica (lineal, angular, piramidal, tetraédrica,
octaédrica, anillos aromáticos). No pretende precisión cristalográfica:
busca que la molécula "se vea bien" y sea didáctica.

Salida: string en formato XYZ, que 3Dmol.js lee con addModel(data, "xyz").
"""

import math

# Radios covalentes aproximados en Å (para estimar longitudes de enlace)
COVALENT_RADII = {
    "H": 0.31, "B": 0.84, "C": 0.76, "N": 0.71, "O": 0.66, "F": 0.57,
    "Si": 1.11, "P": 1.07, "S": 1.05, "Cl": 1.02, "Br": 1.20, "I": 1.39,
    "Li": 1.28, "Na": 1.66, "K": 2.03, "Mg": 1.41, "Ca": 1.76,
}
DEFAULT_RADIUS = 1.0


def _bond_len(a: str, b: str) -> float:
    """Longitud de enlace estimada: suma de radios covalentes."""
    return COVALENT_RADII.get(a, DEFAULT_RADIUS) + COVALENT_RADII.get(b, DEFAULT_RADIUS)


# ── Geometrías VSEPR básicas ─────────────────────────────────────────
# Cada builder devuelve una lista de tuplas (símbolo, x, y, z) en Å.

def _diatomic(a, b):
    d = _bond_len(a, b)
    return [(a, 0.0, 0.0, 0.0), (b, d, 0.0, 0.0)]


def _linear3(izq, centro, der):
    """X—C—X lineal (180°), como CO₂ o N₂O."""
    di = _bond_len(izq, centro)
    dd = _bond_len(centro, der)
    return [(centro, 0.0, 0.0, 0.0), (izq, -di, 0.0, 0.0), (der, dd, 0.0, 0.0)]


def _bent(centro, lat1, lat2, angulo_deg):
    """Angular (H₂O 104.5°, SO₂ 119°, …). Centro en origen."""
    half = math.radians(angulo_deg / 2)
    d1 = _bond_len(centro, lat1)
    d2 = _bond_len(centro, lat2)
    return [
        (centro, 0.0, 0.0, 0.0),
        (lat1, -d1 * math.sin(half), -d1 * math.cos(half), 0.0),
        (lat2,  d2 * math.sin(half), -d2 * math.cos(half), 0.0),
    ]


def _trigonal_planar(centro, lateral):
    """Trigonal plana 120° (BH₃, SO₃)."""
    d = _bond_len(centro, lateral)
    out = [(centro, 0.0, 0.0, 0.0)]
    for ang in (90, 210, 330):
        a = math.radians(ang)
        out.append((lateral, d * math.cos(a), d * math.sin(a), 0.0))
    return out


def _pyramidal(centro, lateral, angulo_deg=107):
    """Pirámide trigonal (NH₃ 107°, PH₃ 93.5°): centro arriba, 3 abajo."""
    d = _bond_len(centro, lateral)
    # Ángulo entre el eje vertical y cada enlace, derivado del ángulo H-X-H
    theta = math.radians(angulo_deg) / 2
    r_xy = d * math.sin(math.radians(70))   # apertura horizontal aproximada
    z = -math.sqrt(max(d * d - r_xy * r_xy, 0.05))
    out = [(centro, 0.0, 0.0, 0.0)]
    for ang in (90, 210, 330):
        a = math.radians(ang)
        out.append((lateral, r_xy * math.cos(a), r_xy * math.sin(a), z))
    return out


def _tetrahedral(centro, lateral):
    """Tetraédrica 109.5° (CH₄, CCl₄, SiH₄)."""
    d = _bond_len(centro, lateral)
    k = d / math.sqrt(3)
    dirs = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    out = [(centro, 0.0, 0.0, 0.0)]
    for dx, dy, dz in dirs:
        out.append((lateral, k * dx, k * dy, k * dz))
    return out


def _octahedral(centro, lateral):
    """Octaédrica 90° (SF₆)."""
    d = _bond_len(centro, lateral)
    dirs = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    out = [(centro, 0.0, 0.0, 0.0)]
    for dx, dy, dz in dirs:
        out.append((lateral, d * dx, d * dy, d * dz))
    return out


def _tetrahedron_p4():
    """P₄: tetraedro regular de fósforo (arista ≈ 2.21 Å)."""
    # Vértices (±1,±1,±1) alternos forman un tetraedro de arista 2√2·k
    k = 2.21 / (2 * math.sqrt(2))
    verts = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    return [("P", k * x, k * y, k * z) for x, y, z in verts]


def _benzene_ring(sustituto=None):
    """
    Anillo bencénico plano (C–C 1.39 Å) con H radiales.
    `sustituto`: lista de (símbolo, dx, dy, dz) que reemplaza al H de la
    posición superior, con desplazamientos relativos a ese carbono.
    """
    rc = 1.39
    out = []
    c_pos = []
    for i in range(6):
        a = math.radians(90 + i * 60)
        x, y = rc * math.cos(a), rc * math.sin(a)
        c_pos.append((x, y))
        out.append(("C", x, y, 0.0))
    dh = _bond_len("C", "H")
    for i, (x, y) in enumerate(c_pos):
        if i == 0 and sustituto is not None:
            for sym, dx, dy, dz in sustituto:
                out.append((sym, x + dx, y + dy, dz))
        else:
            norm = math.hypot(x, y)
            out.append(("H", x + dh * x / norm, y + dh * y / norm, 0.0))
    return out


def _h2o2():
    """H₂O₂ con su torsión característica (conformación gauche)."""
    doo = 1.48
    doh = 0.97
    ang = math.radians(95)
    return [
        ("O", 0.0, 0.0, 0.0),
        ("O", doo, 0.0, 0.0),
        ("H", -doh * math.cos(ang), doh * math.sin(ang), 0.0),
        ("H", doo + doh * math.cos(ang), 0.0, doh * math.sin(ang)),
    ]


def _c2h4():
    """Etileno plano."""
    dcc, dch = 1.33, 1.09
    a = math.radians(120)
    sx, sy = dch * math.cos(a / 2), dch * math.sin(a / 2)
    return [
        ("C", 0.0, 0.0, 0.0), ("C", dcc, 0.0, 0.0),
        ("H", -sx, sy, 0.0), ("H", -sx, -sy, 0.0),
        ("H", dcc + sx, sy, 0.0), ("H", dcc + sx, -sy, 0.0),
    ]


def _c2h2():
    """Acetileno lineal H–C≡C–H."""
    dcc, dch = 1.20, 1.06
    return [
        ("C", 0.0, 0.0, 0.0), ("C", dcc, 0.0, 0.0),
        ("H", -dch, 0.0, 0.0), ("H", dcc + dch, 0.0, 0.0),
    ]


# Direcciones "tetraédricas" para colgar hidrógenos en el builder genérico
_H_DIRS = [
    (0.0, 0.94, 0.34), (0.0, -0.94, 0.34), (0.0, 0.53, -0.85),
    (0.0, -0.53, -0.85), (0.3, 0.0, 0.95), (0.3, 0.0, -0.95),
]


def _generic_from_atoms(atoms):
    """
    Fallback para moléculas sin geometría dedicada:
    átomos pesados en cadena zigzag, hidrógenos repartidos alrededor.
    Es una disposición simple pero legible en 3D.
    """
    heavies = [s for s in atoms if s != "H"]
    n_h = sum(1 for s in atoms if s == "H")
    out = []
    pos_heavy = []

    if not heavies:                       # solo hidrógenos (no debería pasar)
        return [("H", i * 0.74, 0.0, 0.0) for i in range(len(atoms))]

    # Cadena zigzag de pesados en el plano XY
    step_x = 1.30
    for k, sym in enumerate(heavies):
        x = k * step_x
        y = 0.45 if k % 2 else -0.45
        pos_heavy.append((sym, x, y, 0.0))
        out.append((sym, x, y, 0.0))

    # Hidrógenos: reparto equitativo entre los átomos pesados
    if n_h:
        base = n_h // len(heavies)
        extra = n_h % len(heavies)
        h_idx = 0
        for k, (sym, x, y, z) in enumerate(pos_heavy):
            cuota = base + (1 if k < extra else 0)
            d = _bond_len(sym, "H")
            for j in range(cuota):
                dx, dy, dz = _H_DIRS[(j + k) % len(_H_DIRS)]
                out.append(("H", x + d * dx, y + d * dy, z + d * dz))
                h_idx += 1
    return out


# ── Registro por svg_key ─────────────────────────────────────────────

GEOMETRY_BUILDERS = {
    # Diatómicas
    "H2":  lambda: _diatomic("H", "H"),   "O2":  lambda: _diatomic("O", "O"),
    "N2":  lambda: _diatomic("N", "N"),   "F2":  lambda: _diatomic("F", "F"),
    "Cl2": lambda: _diatomic("Cl", "Cl"), "Br2": lambda: _diatomic("Br", "Br"),
    "I2":  lambda: _diatomic("I", "I"),   "HCl": lambda: _diatomic("H", "Cl"),
    "HF":  lambda: _diatomic("H", "F"),   "HBr": lambda: _diatomic("H", "Br"),
    "HI":  lambda: _diatomic("H", "I"),   "CO":  lambda: _diatomic("C", "O"),
    "NO":  lambda: _diatomic("N", "O"),   "NaCl": lambda: _diatomic("Na", "Cl"),
    "LiH": lambda: _diatomic("Li", "H"),  "KBr": lambda: _diatomic("K", "Br"),
    "MgO": lambda: _diatomic("Mg", "O"),  "CaO": lambda: _diatomic("Ca", "O"),
    # Lineales de 3
    "CO2":  lambda: _linear3("O", "C", "O"),
    "N2O":  lambda: _linear3("N", "N", "O"),
    "SiO2": lambda: _linear3("O", "Si", "O"),
    "Na2O": lambda: _bent("O", "Na", "Na", 140),
    # Angulares
    "H2O":  lambda: _bent("O", "H", "H", 104.5),
    "SO2":  lambda: _bent("S", "O", "O", 119),
    "H2S":  lambda: _bent("S", "H", "H", 92),
    "NO2":  lambda: _bent("N", "O", "O", 134),
    "H2O2": _h2o2,
    # Trigonal plana
    "SO3": lambda: _trigonal_planar("S", "O"),
    "BH3": lambda: _trigonal_planar("B", "H"),
    # Piramidal
    "NH3":  lambda: _pyramidal("N", "H", 107),
    "PH3":  lambda: _pyramidal("P", "H", 93.5),
    "PCl3": lambda: _pyramidal("P", "Cl", 100),
    # Tetraédrica
    "CH4":  lambda: _tetrahedral("C", "H"),
    "SiH4": lambda: _tetrahedral("Si", "H"),
    "CCl4": lambda: _tetrahedral("C", "Cl"),
    # Octaédrica
    "SF6": lambda: _octahedral("S", "F"),
    # Especiales
    "P4":   _tetrahedron_p4,
    "C2H2": _c2h2,
    "C2H4": _c2h4,
    # Aromáticos: anillo + sustituyente aproximado
    "C6H6":    lambda: _benzene_ring(),
    "C6H5OH":  lambda: _benzene_ring([("O", 0.0, 1.36, 0.0), ("H", 0.8, 1.95, 0.0)]),
    "C6H5CH3": lambda: _benzene_ring([("C", 0.0, 1.50, 0.0), ("H", 0.9, 2.05, 0.0),
                                      ("H", -0.9, 2.05, 0.0), ("H", 0.0, 1.85, 1.0)]),
    "C6H5NH2": lambda: _benzene_ring([("N", 0.0, 1.40, 0.0), ("H", 0.85, 1.95, 0.0),
                                      ("H", -0.85, 1.95, 0.0)]),
    "C6H5NO2": lambda: _benzene_ring([("N", 0.0, 1.47, 0.0), ("O", 1.05, 2.10, 0.0),
                                      ("O", -1.05, 2.10, 0.0)]),
}


# ── API pública ──────────────────────────────────────────────────────

def get_atoms_3d(svg_key: str, atoms_fallback: list = None) -> list:
    """
    Lista de (símbolo, x, y, z) para la molécula. Usa la geometría dedicada
    si existe; si no, la disposición genérica a partir de la lista de átomos.
    """
    builder = GEOMETRY_BUILDERS.get(svg_key)
    if builder:
        return builder()
    if atoms_fallback:
        return _generic_from_atoms(atoms_fallback)
    return []


def to_xyz(atoms_3d: list, titulo: str = "molecula") -> str:
    """Convierte [(sym,x,y,z), …] al formato XYZ que entiende 3Dmol.js."""
    lines = [str(len(atoms_3d)), titulo]
    for sym, x, y, z in atoms_3d:
        lines.append(f"{sym} {x:.3f} {y:.3f} {z:.3f}")
    return "\n".join(lines)


def get_xyz(svg_key: str, atoms_fallback: list = None, titulo: str = "") -> str:
    """String XYZ listo para incrustar en la página. Vacío si no hay datos."""
    atoms_3d = get_atoms_3d(svg_key, atoms_fallback)
    if not atoms_3d:
        return ""
    return to_xyz(atoms_3d, titulo or svg_key)


def xyz_from_sandbox(atoms: list, escala: float = 60.0) -> str:
    """
    Para el sandbox: convierte los átomos colocados en el lienzo 2D
    [{"sym": "O", "x": 120, "y": 80}, …] a XYZ (plano, z=0), preservando
    la disposición que dibujó el usuario. `escala` = píxeles por Å.
    """
    if not atoms:
        return ""
    # Centrar la molécula para que el visor la encuadre bien
    cx = sum(a["x"] for a in atoms) / len(atoms)
    cy = sum(a["y"] for a in atoms) / len(atoms)
    atoms_3d = [(a["sym"], (a["x"] - cx) / escala, -(a["y"] - cy) / escala, 0.0)
                for a in atoms]
    return to_xyz(atoms_3d, "sandbox")
