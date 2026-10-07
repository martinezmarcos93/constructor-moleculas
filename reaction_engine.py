"""Motor educativo de balanceo de ecuaciones químicas.

Implementa conservación de átomos con aritmética racional. Está pensado para
ecuaciones inorgánicas sencillas sin grupos entre paréntesis en las fórmulas.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
from math import gcd
from functools import reduce

from stoichiometry import parse_formula


def _rref(matrix: list[list[Fraction]]) -> tuple[list[list[Fraction]], list[int]]:
    a = [row[:] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    pivot_cols = []
    pivot_row = 0

    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        divisor = a[pivot_row][col]
        a[pivot_row] = [x / divisor for x in a[pivot_row]]
        for r in range(rows):
            if r == pivot_row:
                continue
            factor = a[r][col]
            if factor:
                a[r] = [a[r][c] - factor * a[pivot_row][c] for c in range(cols)]
        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == rows:
            break
    return a, pivot_cols


def _null_vector(matrix: list[list[Fraction]]) -> list[Fraction]:
    rref, pivots = _rref(matrix)
    cols = len(matrix[0])
    free = [c for c in range(cols) if c not in pivots]
    if len(free) != 1:
        raise ValueError("La ecuación necesita un método de balanceo con más de un grado de libertad.")
    free_col = free[0]
    vector = [Fraction(0) for _ in range(cols)]
    vector[free_col] = Fraction(1)
    for row, pivot_col in enumerate(pivots):
        vector[pivot_col] = -rref[row][free_col]
    return vector


def _integerize(values: list[Fraction]) -> list[int]:
    lcm = 1
    for value in values:
        lcm = lcm * value.denominator // gcd(lcm, value.denominator)
    ints = [int(value * lcm) for value in values]
    common = reduce(gcd, (abs(x) for x in ints if x))
    ints = [x // common for x in ints]
    if all(x < 0 for x in ints):
        ints = [-x for x in ints]
    return ints


def balance_equation(reactants: list[str], products: list[str]) -> dict:
    if not reactants or not products:
        raise ValueError("Una reacción necesita reactivos y productos.")

    all_formulas = [*reactants, *products]
    parsed = [parse_formula(formula) for formula in all_formulas]
    elements = sorted(set().union(*(p.keys() for p in parsed)))
    columns = len(all_formulas)
    matrix = []
    for element in elements:
        row = []
        for index, composition in enumerate(parsed):
            sign = 1 if index < len(reactants) else -1
            row.append(Fraction(sign * composition.get(element, 0)))
        matrix.append(row)

    coefficients = _null_vector(matrix)
    if any(value == 0 for value in coefficients):
        raise ValueError("No se obtuvo un coeficiente positivo para todas las sustancias.")

    integers = _integerize(coefficients)
    if any(value <= 0 for value in integers):
        raise ValueError("No se obtuvo una solución positiva para el balanceo.")

    left = integers[:len(reactants)]
    right = integers[len(reactants):]

    return {
        "reactants": [{"formula": f, "coefficient": c} for f, c in zip(reactants, left)],
        "products": [{"formula": f, "coefficient": c} for f, c in zip(products, right)],
        "coefficients": integers,
        "equation": " + ".join(_format_term(c, f) for c, f in zip(left, reactants))
                    + " → "
                    + " + ".join(_format_term(c, f) for c, f in zip(right, products)),
        "conserved": _conserved_elements(parsed, integers, len(reactants)),
    }


def _format_term(coefficient: int, formula: str) -> str:
    return formula if coefficient == 1 else f"{coefficient}{formula}"


def _conserved_elements(parsed: list[dict[str, int]], coefficients: list[int], split: int) -> bool:
    for element in set().union(*(p.keys() for p in parsed)):
        left = sum(coefficients[i] * parsed[i].get(element, 0) for i in range(split))
        right = sum(coefficients[i] * parsed[i].get(element, 0) for i in range(split, len(parsed)))
        if left != right:
            return False
    return True
