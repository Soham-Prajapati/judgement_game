def get_illegal_bid(
    current_bids: dict[str, int],
    total_cards: int,
    is_last_bidder: bool,
) -> int | None:
    if not is_last_bidder:
        return None
    return total_cards - sum(current_bids.values())


def validate_bid(bid: int, illegal_bid: int | None, total_cards: int) -> bool:
    if bid < 0 or bid > total_cards:
        return False
    if illegal_bid is None:
        return True
    return bid != illegal_bid
