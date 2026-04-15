from typing import List, Tuple, Dict
from .deck import Card, RANKS, SUITS

# Card rank value map for comparison
RANK_VALUE_MAP = {rank: idx for idx, rank in enumerate(RANKS)}

def get_trick_winner(trick: List[Tuple[str, Card]], trump_suit: str) -> str:
    """
    Determines the winner of a trick.
    Input: trick = [(player_id, Card), ...]
    Output: player_id of the winner
    """
    if not trick:
        return ""

    leader_id, lead_card = trick[0]
    lead_suit = lead_card.suit

    winner_id = leader_id
    best_card = lead_card

    for player_id, card in trick[1:]:
        # If trump played
        if card.suit == trump_suit:
            # If current best is NOT trump, new card is better
            if best_card.suit != trump_suit:
                best_card = card
                winner_id = player_id
            # If current best IS trump, higher rank wins
            elif RANK_VALUE_MAP[card.rank] > RANK_VALUE_MAP[best_card.rank]:
                best_card = card
                winner_id = player_id
        # If lead suit played and current best is NOT trump
        elif card.suit == lead_suit and best_card.suit != trump_suit:
            # Higher rank of lead suit wins
            if RANK_VALUE_MAP[card.rank] > RANK_VALUE_MAP[best_card.rank]:
                best_card = card
                winner_id = player_id

    return winner_id

def is_valid_play(card: Card, player_hand: List[Card], trick: List[Tuple[str, Card]]) -> bool:
    """
    Validates if a card played is valid according to following suit rules.
    """
    if not trick:
        return True # Lead card is always valid if in hand

    lead_card_id, lead_card = trick[0]
    lead_suit = lead_card.suit

    # If following suit
    if card.suit == lead_suit:
        return True

    # If NOT following suit, check if player has any card of lead suit
    has_lead_suit = any(c.suit == lead_suit for c in player_hand)
    if has_lead_suit:
        return False # Must follow suit if you have it

    return True
