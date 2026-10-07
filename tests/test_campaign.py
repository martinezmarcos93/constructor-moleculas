from atomos_perdidos.game.campaign import campaign_snapshot, current_chapter, reward_for_chapter


def test_campaign_starts_at_first_chapter():
    snap = campaign_snapshot({"mastery": {}})
    assert snap["chapters"][0]["unlocked"] is True
    assert current_chapter({"mastery": {}})["id"] == "capitulo-1"


def test_campaign_unlocks_later_chapters_from_mastery():
    data = {"mastery": {
        "atomos": {"value": 100},
        "tabla_periodica": {"value": 25},
        "enlaces": {"value": 25},
        "moleculas": {"value": 25},
        "formulas": {"value": 25},
        "reacciones": {"value": 25},
        "laboratorio": {"value": 60},
    }}
    snap = campaign_snapshot(data)
    unlocked = {c["id"] for c in snap["chapters"] if c["unlocked"]}
    assert "capitulo-6" in unlocked
    assert "capitulo-7" in unlocked


def test_chapter_rewards_are_defined():
    reward = reward_for_chapter("capitulo-6")
    assert reward["xp"] > 0
    assert reward["credits"] > 0
