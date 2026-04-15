from game.trump import get_trump_suit

def test_get_trump_suit():
    assert get_trump_suit(1) == "S"
    assert get_trump_suit(2) == "D"
    assert get_trump_suit(3) == "H"
    assert get_trump_suit(4) == "C"
    assert get_trump_suit(5) == "S"
    assert get_trump_suit(6) == "D"
