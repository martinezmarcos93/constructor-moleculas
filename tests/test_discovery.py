from atomos_perdidos.game.discovery_engine import discover, snapshot


def test_discovery_is_idempotent():
    molecule = {"id": "water", "name": "Agua", "formula": "H2O"}
    items, first = discover([], molecule)
    assert first is True
    items, second = discover(items, molecule)
    assert second is False
    assert len(items) == 1


def test_discovery_snapshot():
    data = snapshot([{"molecule_id": "water"}], 10)
    assert data["discovered"] == 1
    assert data["total"] == 10
    assert data["percent"] == 10.0
