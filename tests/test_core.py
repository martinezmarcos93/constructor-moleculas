"""Pruebas del núcleo de química y progresión."""
from chemistry_rules import analyze_formula, format_formula
from progression import Progression

def test_format_formula_conventions():
    assert format_formula(["H", "H", "O"]) == "H₂O"
    assert format_formula(["Na", "Cl"]) == "NaCl"
    assert format_formula(["H", "H", "S", "O", "O", "O", "O"]) == "H₂SO₄"

def test_known_formula():
    result = analyze_formula(["H", "H", "O"], {"H₂O"})
    assert result.known and result.plausible

def test_unknown_but_structurally_supported_formula():
    result = analyze_formula(["Na", "F"], {"H₂O"})
    assert not result.known and result.plausible

def test_progression_unlocks_in_order():
    p = Progression()
    assert p.unlocked_domains() == ["atomos", "tabla_periodica"]
    p.register("tabla_periodica", True, 25)
    assert "enlaces" in p.unlocked_domains()


def test_challenges_include_geometry_mode():
    from challenge_model import build_challenges
    molecules = {
        "medium": [{
            "id": "H2O",
            "name": "Agua",
            "atoms": ["H", "H", "O"],
            "svg_key": "H2O",
        }]
    }
    challenges = build_challenges(molecules)
    geometry = next(c for c in challenges if c.mode == "geometry")
    assert geometry.answer == "angular"
    assert "molecular_geometry" in geometry.concepts
