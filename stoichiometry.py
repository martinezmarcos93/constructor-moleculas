"""Estequiometría básica para el laboratorio educativo."""
from __future__ import annotations

import re
from collections import Counter
from periodic_table import ELEMENTS

_SUBSCRIPT = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")


def parse_formula(formula: str) -> dict[str, int]:
    """Parsea fórmulas simples sin paréntesis, por ejemplo H2SO4 o Ca(OH)2 no."""
    if not isinstance(formula, str) or not formula.strip():
        raise ValueError("La fórmula está vacía.")
    formula = formula.strip()
    if "(" in formula or ")" in formula:
        raise ValueError("Esta versión aún no soporta grupos entre paréntesis.")
    formula = formula.translate(_SUBSCRIPT)
    tokens = re.findall(r"([A-Z][a-z]?)(\d*)", formula)
    if not tokens or "".join(symbol + count for symbol, count in tokens) != formula:
        raise ValueError("Fórmula química no reconocida.")
    counts = Counter()
    for symbol, raw_count in tokens:
        if not any(el["symbol"] == symbol for el in ELEMENTS.values()):
            raise ValueError(f"Elemento desconocido: {symbol}.")
        counts[symbol] += int(raw_count or "1")
    return dict(counts)


def molar_mass(formula: str) -> float:
    counts = parse_formula(formula)
    by_symbol = {el["symbol"]: el for el in ELEMENTS.values()}
    return sum(by_symbol[s]["mass"] * n for s, n in counts.items())


def mass_percentages(formula: str) -> dict[str, float]:
    counts = parse_formula(formula)
    by_symbol = {el["symbol"]: el for el in ELEMENTS.values()}
    total = molar_mass(formula)
    return {
        symbol: round(by_symbol[symbol]["mass"] * count / total * 100, 4)
        for symbol, count in counts.items()
    }


def analyze_formula_stoichiometry(formula: str) -> dict:
    counts = parse_formula(formula)
    mass = molar_mass(formula)
    return {
        "formula": formula,
        "elements": counts,
        "molar_mass": round(mass, 5),
        "mass_percentages": mass_percentages(formula),
    }
