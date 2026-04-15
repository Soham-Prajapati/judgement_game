from typing import List, Optional

def get_illegal_bid(total_cards: int, current_bids: List[int], is_last_bidder: bool) -> Optional[int]:
    """
    Returns the illegal bid for the last bidder, or None if not the last bidder.
    Rule: The sum of all bids in a round cannot be equal to the number of cards dealt in that round.
    """
    if not is_last_bidder:
        return None

    current_sum = sum(current_bids)
    illegal_bid = total_cards - current_sum

    if 0 <= illegal_bid <= total_cards:
        return illegal_bid
    else:
        return None

def is_valid_bid(bid: int, total_cards: int, current_bids: List[int], is_last_bidder: bool) -> bool:
    """
    Checks if a bid is valid.
    """
    if bid < 0 or bid > total_cards:
        return False

    illegal_bid = get_illegal_bid(total_cards, current_bids, is_last_bidder)
    if illegal_bid is not None and bid == illegal_bid:
        return False

    return True
