from atomos_perdidos.game.mission_engine import generate_mission, evaluate_mission, list_missions


def test_generated_missions_are_reproducible():
    mission = generate_mission("fabrica_agua", 2, "seed")
    again = generate_mission(mission["id"], 2, "different-seed")
    assert mission["id"] == again["id"]
    assert mission["target_moles"] == again["target_moles"]


def test_water_mission_can_be_completed_at_stoichiometric_ratio():
    mission = generate_mission("fabrica_agua", 1, "fixed")
    target = mission["target_moles"]
    result = evaluate_mission(mission, {"H2": target * 2, "O2": target}, "ninguno")
    assert result["completed"] is True
    assert result["stoichiometric_tie"] is True
    assert result["score"] == 100


def test_mission_rejects_excessive_waste():
    mission = generate_mission("fabrica_agua", 4, "waste")
    result = evaluate_mission(mission, {"H2": mission["target_moles"] * 10, "O2": mission["target_moles"]})
    assert result["status"] == "failed"
    assert result["constraints"]["target_met"] is True


def test_catalog_contains_multiple_difficulties():
    missions = list_missions()
    assert len(missions) >= 12
    assert {m["difficulty"] for m in missions} == {1, 2, 3}


def test_expanded_reaction_templates_generate():
    for template in ("horno_metano", "neutralizacion", "calcinacion"):
        mission = generate_mission(template, 2, "coverage")
        assert mission["reactants"]
        assert mission["products"]


def test_mission_rejects_non_finite_quantities():
    import pytest
    mission = generate_mission("fabrica_agua", 1, "finite")
    with pytest.raises(ValueError, match="positiva y finita"):
        evaluate_mission(mission, {"H2": float("inf"), "O2": 1})
