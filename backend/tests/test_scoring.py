from game.scoring import calculate_round_scores, update_cumulative_scores


def test_calculate_round_scores_exact_bid_only() -> None:
    bids = {"alice": 2, "bob": 1, "charlie": 0}
    tricks = {"alice": 2, "bob": 0, "charlie": 0}
    assert calculate_round_scores(bids, tricks) == {"alice": 10, "bob": 0, "charlie": 10}


def test_update_cumulative_scores_appends_round_values() -> None:
    existing = {"alice": [10], "bob": [0]}
    round_scores = {"alice": 0, "bob": 10, "charlie": 10}

    updated = update_cumulative_scores(existing, round_scores)

    assert updated["alice"] == [10, 0]
    assert updated["bob"] == [0, 10]
    assert updated["charlie"] == [10]
