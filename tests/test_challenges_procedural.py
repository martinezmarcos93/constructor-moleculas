from atomos_perdidos.game.challenge_model import generate_procedural_challenge
from atomos_perdidos.data.molecules import MOLECULES


def test_procedural_challenge_is_reproducible():
    a = generate_procedural_challenge(MOLECULES, 3, 42)
    b = generate_procedural_challenge(MOLECULES, 3, 42)
    assert a == b
    assert a["difficulty"] == 3
    assert a["answer"]
