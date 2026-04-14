import pytest

from game.tricks import determine_trick_winner, get_playable_cards, must_follow_suit


def test_determine_winner_lead_suit_when_no_trump() -> None:
    trick = [
        {"username": "alice", "card": {"suit": "hearts", "value": "10"}},
        {"username": "bob", "card": {"suit": "hearts", "value": "K"}},
        {"username": "charlie", "card": {"suit": "clubs", "value": "A"}},
    ]
    assert determine_trick_winner(trick, trump_suit="spades", lead_suit="hearts") == "bob"


def test_determine_winner_uses_highest_trump() -> None:
    trick = [
        {"username": "alice", "card": {"suit": "hearts", "value": "A"}},
        {"username": "bob", "card": {"suit": "spades", "value": "2"}},
        {"username": "charlie", "card": {"suit": "spades", "value": "Q"}},
    ]
    assert determine_trick_winner(trick, trump_suit="spades", lead_suit="hearts") == "charlie"


def test_get_playable_cards_enforces_lead_suit() -> None:
    hand = [
        {"suit": "hearts", "value": "2"},
        {"suit": "clubs", "value": "A"},
        {"suit": "hearts", "value": "K"},
    ]

    assert must_follow_suit(hand, "hearts")
    assert get_playable_cards(hand, "hearts") == [
        {"suit": "hearts", "value": "2"},
        {"suit": "hearts", "value": "K"},
    ]


def test_determine_winner_rejects_empty_trick() -> None:
    with pytest.raises(ValueError):
        determine_trick_winner([], trump_suit="spades", lead_suit="hearts")