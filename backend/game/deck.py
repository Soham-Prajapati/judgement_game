import random
from typing import List, Tuple

SUITS = ["S", "D", "H", "C"]  # Spades, Diamonds, Hearts, Clubs
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

class Card:
    def __init__(self, suit: str, rank: str):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def to_dict(self):
        return {"suit": self.suit, "rank": self.rank}

def create_deck() -> List[Card]:
    return [Card(suit, rank) for suit in SUITS for rank in RANKS]

def shuffle_deck(deck: List[Card]):
    random.shuffle(deck)

def deal_cards(deck: List[Card], num_players: int, cards_per_player: int) -> Tuple[List[List[Card]], List[Card]]:
    players_hands = [[] for _ in range(num_players)]
    for _ in range(cards_per_player):
        for player_idx in range(num_players):
            if deck:
                players_hands[player_idx].append(deck.pop(0))
    return players_hands, deck
