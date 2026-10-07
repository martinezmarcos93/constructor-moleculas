"""Modelo explícito de estructuras moleculares para Átomos Perdidos.

No intenta ser un motor químico profesional. Su objetivo es representar
átomos + enlaces + orden de enlace y producir validaciones pedagógicas
deterministas para el laboratorio.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from collections import Counter
from typing import Iterable

from atomos_perdidos.core.chemistry_rules import COMMON_VALENCES, IONIC_CHARGES, format_formula


@dataclass(frozen=True)
class AtomNode:
    id: str
    symbol: str


@dataclass(frozen=True)
class Bond:
    a: str
    b: str
    order: int = 1
    kind: str = "covalent"

    def normalized_pair(self) -> tuple[str, str]:
        return tuple(sorted((self.a, self.b)))


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    severity: str
    message: str


@dataclass
class MoleculeStructure:
    atoms: dict[str, AtomNode] = field(default_factory=dict)
    bonds: list[Bond] = field(default_factory=list)

    def add_atom(self, atom_id: str, symbol: str) -> "MoleculeStructure":
        symbol = symbol.strip().capitalize()
        if not symbol:
            raise ValueError("El símbolo del átomo no puede estar vacío.")
        if atom_id in self.atoms:
            raise ValueError(f"Ya existe el átomo {atom_id}.")
        self.atoms[atom_id] = AtomNode(atom_id, symbol)
        return self

    def add_bond(self, a: str, b: str, order: int = 1, kind: str = "covalent") -> "MoleculeStructure":
        if a == b:
            raise ValueError("Un átomo no puede enlazarse consigo mismo.")
        if a not in self.atoms or b not in self.atoms:
            raise ValueError("El enlace referencia un átomo inexistente.")
        if order not in (1, 2, 3):
            raise ValueError("El orden de enlace debe ser 1, 2 o 3.")
        if kind not in {"covalent", "ionic"}:
            raise ValueError("Tipo de enlace no soportado.")
        pair = tuple(sorted((a, b)))
        if any(bond.normalized_pair() == pair for bond in self.bonds):
            raise ValueError("Ya existe un enlace entre esos átomos.")
        self.bonds.append(Bond(a, b, order, kind))
        return self

    def bond_order_sum(self, atom_id: str) -> int:
        return sum(b.order for b in self.bonds
                   if b.kind == "covalent" and atom_id in (b.a, b.b))

    def neighbors(self, atom_id: str) -> list[str]:
        result = []
        for bond in self.bonds:
            if bond.a == atom_id:
                result.append(bond.b)
            elif bond.b == atom_id:
                result.append(bond.a)
        return result

    def is_connected(self) -> bool:
        if not self.atoms:
            return False
        seen = set()
        pending = [next(iter(self.atoms))]
        while pending:
            current = pending.pop()
            if current in seen:
                continue
            seen.add(current)
            pending.extend(n for n in self.neighbors(current) if n not in seen)
        return len(seen) == len(self.atoms)

    def formula(self) -> str:
        return format_formula([atom.symbol for atom in self.atoms.values()])

    def validate(self) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if not self.atoms:
            return [ValidationIssue("empty", "error", "La estructura no contiene átomos.")]

        if len(self.atoms) > 1 and not self.is_connected():
            issues.append(ValidationIssue(
                "disconnected", "error",
                "La estructura tiene grupos de átomos desconectados."
            ))

        for atom in self.atoms.values():
            incident = [b for b in self.bonds if atom.id in (b.a, b.b)]
            if any(b.kind == "ionic" for b in incident):
                continue
            valences = COMMON_VALENCES.get(atom.symbol)
            if not valences:
                issues.append(ValidationIssue(
                    "unknown_valence", "warning",
                    f"No hay una regla didáctica de valencia para {atom.symbol}."
                ))
                continue
            used = self.bond_order_sum(atom.id)
            if used == 0 and len(self.atoms) > 1:
                issues.append(ValidationIssue(
                    "isolated_atom", "error",
                    f"{atom.symbol} no participa de ningún enlace."
                ))
            elif used not in valences:
                max_valence = max(valences)
                severity = "error" if used > max_valence else "warning"
                issues.append(ValidationIssue(
                    "valence",
                    severity,
                    f"{atom.symbol} usa {used} unidades de enlace; "
                    f"las valencias didácticas disponibles son {valences}."
                ))

        return issues

    def is_valid(self) -> bool:
        return not any(issue.severity == "error" for issue in self.validate())

    def summary(self) -> dict:
        return {
            "formula": self.formula(),
            "atoms": [{"id": a.id, "symbol": a.symbol} for a in self.atoms.values()],
            "bonds": [
                {"a": b.a, "b": b.b, "order": b.order, "kind": b.kind}
                for b in self.bonds
            ],
            "valid": self.is_valid(),
            "issues": [
                {"code": i.code, "severity": i.severity, "message": i.message}
                for i in self.validate()
            ],
        }


def structure_from_formula(symbols: Iterable[str], bonds: Iterable[tuple[int, int, int]]):
    """Construye una estructura desde posiciones de una lista de símbolos."""
    structure = MoleculeStructure()
    normalized = [s.strip().capitalize() for s in symbols]
    for index, symbol in enumerate(normalized):
        structure.add_atom(str(index), symbol)
    for a, b, order in bonds:
        structure.add_bond(str(a), str(b), order)
    return structure


def common_ionic_pair(symbols: Iterable[str]) -> bool:
    counts = Counter(s.strip().capitalize() for s in symbols)
    if len(counts) != 2:
        return False
    items = list(counts.items())
    if not all(symbol in IONIC_CHARGES for symbol, _ in items):
        return False
    (a, na), (b, nb) = items
    return any(x * na + y * nb == 0 for x in IONIC_CHARGES[a] for y in IONIC_CHARGES[b])
