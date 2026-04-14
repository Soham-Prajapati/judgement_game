from game.deck import create_deck, deal_cards, shuffle_deck


def test_create_deck_has_52_unique_cards() -> None:
    deck = create_deck()
    assert len(deck) == 52
    assert len({(card["suit"], card["value"]) for card in deck}) == 52


def test_shuffle_keeps_same_card_set() -> None:
    deck = create_deck()
    shuffled = shuffle_deck(deck)
    assert len(shuffled) == 52
    assert sorted((card["suit"], card["value"]) for card in shuffled) == sorted(
        (card["suit"], card["value"]) for card in deck
    )


def test_deal_cards_distributes_evenly() -> None:
    deck = create_deck()
    hands = deal_cards(deck, players=["alice", "bob"], cards_per_player=5)
    assert len(hands["alice"]) == 5
    assert len(hands["bob"]) == 5