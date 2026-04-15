from game.scoring import calculate_round_score

def test_calculate_round_score():
    assert calculate_round_score(2, 2) == 10
    assert calculate_round_score(2, 3) == 0
    assert calculate_round_score(0, 0) == 10
    assert calculate_round_score(0, 1) == 0
