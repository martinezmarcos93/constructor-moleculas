from __future__ import annotations
"""Sistema de descubrimiento y colección de moléculas."""
from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class Discovery:
    molecule_id: str
    name: str
    formula: str
    first_seen: bool = True

    def serialize(self) -> dict:
        return asdict(self)


def discover(existing: list[dict], molecule: dict) -> tuple[list[dict], bool]:
    current = list(existing or [])
    molecule_id = str(molecule.get("id", ""))
    if not molecule_id:
        raise ValueError("La molécula no tiene id.")
    if any(str(item.get("molecule_id")) == molecule_id for item in current):
        return current, False
    current.append(Discovery(
        molecule_id=molecule_id,
        name=str(molecule.get("name", molecule_id)),
        formula=str(molecule.get("formula", "?")),
    ).serialize())
    return current, True


def snapshot(existing: list[dict], total: int) -> dict:
    items = list(existing or [])
    return {
        "discovered": len(items),
        "total": max(0, int(total)),
        "percent": round(len(items) / max(1, int(total)) * 100, 1),
        "items": items,
    }
