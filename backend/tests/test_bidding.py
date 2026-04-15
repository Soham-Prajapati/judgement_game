from game.bidding import get_illegal_bid, is_valid_bid

def test_get_illegal_bid():
    total_cards = 7
    current_bids = [1, 2, 1]
    # Not last bidder
    assert get_illegal_bid(total_cards, current_bids, False) == None
    # Last bidder
    # Current sum = 4. Illegal = 7 - 4 = 3
    assert get_illegal_bid(total_cards, current_bids, True) == 3

def test_is_valid_bid():
    total_cards = 7
    current_bids = [1, 2, 1]
    
    # Valid bid, not last
    assert is_valid_bid(3, total_cards, current_bids, False) == True
    # Valid bid, last
    assert is_valid_bid(2, total_cards, current_bids, True) == True
    # Invalid bid (illegal), last
    assert is_valid_bid(3, total_cards, current_bids, True) == False
    # Invalid bid (out of range)
    assert is_valid_bid(8, total_cards, current_bids, False) == False
    assert is_valid_bid(-1, total_cards, current_bids, False) == False
