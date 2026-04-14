from __future__ import annotations

import random

SUITS = ("spades", "diamonds", "hearts", "clubs")
VALUES = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")


def create_deck() -> list[dict[str, str]]:
    return [{"suit": suit, "value": value} for suit in SUITS for value in VALUES]


def shuffle_deck(deck: list[dict[str, str]]) -> list[dict[str, str]]:
    shuffled = deck.copy()
    random.shuffle(shuffled)
    return shuffled


def deal_cards(
    deck: list[dict[str, str]],
    players: list[str],
    cards_per_player: int,
) -> dict[str, list[dict[str, str]]]:
    total_needed = len(players) * cards_per_player
    if total_needed > len(deck):
        raise ValueError("Not enough cards in deck")

    hands: dict[str, list[dict[str, str]]] = {player: [] for player in players}
    deck_index = 0
    for _ in range(cards_per_player):
        for player in players:
            hands[player].append(deck[deck_index])
            deck_index += 1
    return hands
