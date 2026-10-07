from mission_engine import generate_mission, evaluate_mission, list_missions


def test_generated_missions_are_reproducible():
    mission = generate_mission("fabrica_agua", 2, "seed")
    again = generate_mission(mission["id"], 2, "different-seed")
    assert mission["id"] == again["id"]
    assert mission["target_moles"] == again["target_moles"]


def test_water_mission_can_be_completed_at_stoichiometric_ratio():
    mission = generate_mission("fabrica_agua", 1, "fixed")
    target = mission["target_moles"]
    result = evaluate_mission(mission, {"H2": target * 2, "O2": target}, "H2")
    assert result["completed"] is True
    assert result["limiting_reagent"] == "O2"
    assert result["score"] >= 90


def test_mission_rejects_excessive_waste():
    mission = generate_mission("fabrica_agua", 4, "waste")
    result = evaluate_mission(mission, {"H2": mission["target_moles"] * 10, "O2": mission["target_moles"]})
    assert result["status"] == "failed"
    assert result["constraints"]["target_met"] is True


def test_catalog_contains_multiple_difficulties():
    missions = list_missions()
    assert len(missions) >= 12
    assert {m["difficulty"] for m in missions} == {1, 2, 3}\n\n\ndef test_expanded_reaction_templates_generate():\n    from mission_engine import generate_mission\n    for template in ("horno_metano", "neutralizacion", "calcinacion"):\n        mission = generate_mission(template, 2, "coverage")\n        assert mission["reactants"]\n        assert mission["products"]
