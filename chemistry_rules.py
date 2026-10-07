"""Reglas químicas básicas para Átomos Perdidos."""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass

COMMON_VALENCES = {
    "H": (1,), "B": (3,), "C": (4,), "N": (3, 5), "O": (2,),
    "F": (1,), "Si": (4,), "P": (3, 5), "S": (2, 4, 6),
    "Cl": (1,), "Br": (1,), "I": (1,), "Li": (1,), "Na": (1,),
    "K": (1,), "Mg": (2,), "Ca": (2,),
}
IONIC_CHARGES = {
    "Li": (1,), "Na": (1,), "K": (1,), "Mg": (2,), "Ca": (2,),
    "F": (-1,), "Cl": (-1,), "Br": (-1,), "I": (-1,), "O": (-2,), "S": (-2,),
}

@dataclass(frozen=True)
class FormulaAnalysis:
    formula: str
    elements: dict[str, int]
    known: bool
    plausible: bool
    message: str

def normalize_symbols(symbols: list[str]) -> list[str]:
    return [s.strip().capitalize() for s in symbols if isinstance(s, str) and s.strip()]

def count_elements(symbols: list[str]) -> Counter:
    return Counter(normalize_symbols(symbols))

def format_formula(symbols: list[str]) -> str:
    counts = count_elements(symbols)
    ordered = []
    if "C" in counts:
        ordered.append("C")
        if "H" in counts:
            ordered.append("H")
        ordered.extend(sorted(k for k in counts if k not in {"C", "H"}))
    else:
        metals = {"Li", "Na", "K", "Mg", "Ca"}
        ordered.extend(sorted(k for k in counts if k in metals))
        ordered.extend(sorted(k for k in counts if k not in metals))
    subs = "₀₁₂₃₄₅₆₇₈₉"
    return "".join(
        symbol + ("" if counts[symbol] == 1 else "".join(subs[int(d)] for d in str(counts[symbol])))
        for symbol in ordered
    )

def binary_ionic_plausible(elements: dict[str, int]) -> bool:
    if len(elements) != 2:
        return False
    a, b = list(elements)
    charges_a, charges_b = IONIC_CHARGES.get(a), IONIC_CHARGES.get(b)
    if not charges_a or not charges_b:
        return False
    return any(x * elements[a] + y * elements[b] == 0 for x in charges_a for y in charges_b)

def analyze_formula(symbols: list[str], known_formulas: set[str] | None = None) -> FormulaAnalysis:
    normalized = normalize_symbols(symbols)
    formula = format_formula(normalized)
    elements = dict(count_elements(normalized))
    if not normalized:
        return FormulaAnalysis("", elements, False, False, "No hay átomos.")
    known = formula in (known_formulas or set())
    if known:
        return FormulaAnalysis(formula, elements, True, True, "Molécula conocida por Átomos Perdidos.")
    if len(elements) == 2 and binary_ionic_plausible(elements):
        return FormulaAnalysis(formula, elements, False, True, "Proporción compatible con un compuesto iónico binario.")
    unknown = [s for s in elements if s not in COMMON_VALENCES]
    if unknown:
        return FormulaAnalysis(formula, elements, False, False, f"No tengo una regla didáctica suficiente para: {', '.join(unknown)}.")
    return FormulaAnalysis(formula, elements, False, True, "La fórmula usa elementos conocidos; la estructura debe comprobarse mediante enlaces.")

def available_valences(symbol: str) -> tuple[int, ...]:
    return COMMON_VALENCES.get(symbol.strip().capitalize(), ())
