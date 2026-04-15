def calculate_round_score(bid: int, tricks_won: int) -> int:
    """
    Calculates the score for a round.
    Rule: +10 if exactly hit bid, else 0.
    """
    if bid == tricks_won:
        return 10
    else:
        return 0
