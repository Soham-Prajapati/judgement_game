from game.tricks import get_trick_winner, is_valid_play
from game.deck import Card

def test_get_trick_winner_no_trump():
    trump_suit = "H"
    trick = [
        ("p1", Card("S", "A")),
        ("p2", Card("S", "K")),
        ("p3", Card("S", "10")),
        ("p4", Card("S", "2"))
    ]
    # Spades lead, Ace is highest
    assert get_trick_winner(trick, trump_suit) == "p1"

def test_get_trick_winner_with_trump():
    trump_suit = "H"
    trick = [
        ("p1", Card("S", "A")),
        ("p2", Card("S", "K")),
        ("p3", Card("H", "2")), # Trumped
        ("p4", Card("S", "Q"))
    ]
    # Spades lead, but p3 played a trump
    assert get_trick_winner(trick, trump_suit) == "p3"

def test_get_trick_winner_highest_trump():
    trump_suit = "H"
    trick = [
        ("p1", Card("S", "A")),
        ("p2", Card("H", "K")), # Higher trump
        ("p3", Card("H", "2")), # Lower trump
        ("p4", Card("S", "Q"))
    ]
    assert get_trick_winner(trick, trump_suit) == "p2"

def test_is_valid_play_following_suit():
    player_hand = [Card("S", "10"), Card("H", "A")]
    trick = [("p1", Card("S", "K"))]
    # Player plays S10, which follows suit
    assert is_valid_play(Card("S", "10"), player_hand, trick) == True

def test_is_valid_play_violating_suit():
    player_hand = [Card("S", "10"), Card("H", "A")]
    trick = [("p1", Card("S", "K"))]
    # Player plays HA but HAS S10 (lead suit)
    assert is_valid_play(Card("H", "A"), player_hand, trick) == False

def test_is_valid_play_no_suit_to_follow():
    player_hand = [Card("D", "10"), Card("H", "A")]
    trick = [("p1", Card("S", "K"))]
    # Player plays HA and does NOT HAVE S (lead suit)
    assert is_valid_play(Card("H", "A"), player_hand, trick) == True
