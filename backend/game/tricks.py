from __future__ import annotations

RANK_ORDER = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def must_follow_suit(hand: list[dict[str, str]], lead_suit: str) -> bool:
    return any(card["suit"] == lead_suit for card in hand)


def get_playable_cards(
    hand: list[dict[str, str]],
    lead_suit: str | None,
) -> list[dict[str, str]]:
    if lead_suit is None:
        return hand
    if not must_follow_suit(hand, lead_suit):
        return hand
    return [card for card in hand if card["suit"] == lead_suit]


def determine_trick_winner(
    trick_pile: list[dict[str, str] | dict[str, dict[str, str]]],
    trump_suit: str,
    lead_suit: str,
) -> str:
    if not trick_pile:
        raise ValueError("trick_pile must not be empty")

    normalized: list[dict[str, str | dict[str, str]]] = []
    for item in trick_pile:
        # Supports {"username": ..., "card": {...}} entries.
        if "username" in item and "card" in item:
            normalized.append(item)
            continue
        if "player" in item and "card" in item:
            normalized.append({"username": item["player"], "card": item["card"]})
            continue
        raise ValueError("invalid trick item format")

    trump_cards = [
        item for item in normalized if item["card"]["suit"] == trump_suit  # type: ignore[index]
    ]
    candidate_cards = trump_cards or [
        item for item in normalized if item["card"]["suit"] == lead_suit  # type: ignore[index]
    ]

    winner_item = max(
        candidate_cards,
        key=lambda item: RANK_ORDER[item["card"]["value"]],  # type: ignore[index]
    )
    return str(winner_item["username"])