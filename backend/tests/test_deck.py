from game.deck import create_deck, shuffle_deck, deal_cards, Card

def test_create_deck():
    deck = create_deck()
    assert len(deck) == 52
    assert isinstance(deck[0], Card)

def test_shuffle_deck():
    deck1 = create_deck()
    deck2 = create_deck()
    shuffle_deck(deck2)
    # Theoretically possible to be same but extremely unlikely
    assert [str(c) for c in deck1] != [str(c) for c in deck2]

def test_deal_cards():
    deck = create_deck()
    num_players = 4
    cards_per_player = 7
    hands, remaining_deck = deal_cards(deck, num_players, cards_per_player)
    
    assert len(hands) == 4
    for hand in hands:
        assert len(hand) == 7
    assert len(remaining_deck) == 52 - (4 * 7)
