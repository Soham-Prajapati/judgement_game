from .deck import SUITS

def get_trump_suit(round_number: int) -> str:
    """
    Returns the trump suit for a given round number.
    Rotation: Spades (S) -> Diamonds (D) -> Hearts (H) -> Clubs (C)
    """
    # Round numbering starts at 1
    # Modulo operator returns 0, 1, 2, 3
    # Mapping to SUITS: S, D, H, C
    idx = (round_number - 1) % len(SUITS)
    return SUITS[idx]
