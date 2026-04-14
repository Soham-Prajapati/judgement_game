import pytest

from game.trump import get_trump_for_round


def test_trump_rotation_cycles() -> None:
    assert get_trump_for_round(1) == "spades"
    assert get_trump_for_round(2) == "diamonds"
    assert get_trump_for_round(3) == "hearts"
    assert get_trump_for_round(4) == "clubs"
    assert get_trump_for_round(5) == "spades"


def test_invalid_round_raises() -> None:
    with pytest.raises(ValueError):
        get_trump_for_round(0)
