def calculate_round_scores(bids: dict[str, int], tricks_won: dict[str, int]) -> dict[str, int]:
    round_scores: dict[str, int] = {}
    for username, bid in bids.items():
        won = tricks_won.get(username, 0)
        round_scores[username] = 10 if bid == won else 0
    return round_scores


def update_cumulative_scores(
    existing: dict[str, list[int]],
    round_scores: dict[str, int],
) -> dict[str, list[int]]:
    merged = {player: scores.copy() for player, scores in existing.items()}
    for username, score in round_scores.items():
        merged.setdefault(username, []).append(score)
    return merged
