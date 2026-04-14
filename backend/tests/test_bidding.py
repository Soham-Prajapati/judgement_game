from game.bidding import get_illegal_bid, validate_bid


def test_illegal_bid_for_last_bidder() -> None:
    current_bids = {"alice": 2, "bob": 1}
    illegal = get_illegal_bid(current_bids, total_cards=5, is_last_bidder=True)
    assert illegal == 2


def test_no_illegal_bid_when_not_last_bidder() -> None:
    current_bids = {"alice": 2, "bob": 1}
    assert get_illegal_bid(current_bids, total_cards=5, is_last_bidder=False) is None


def test_validate_bid_respects_illegal_value() -> None:
    assert validate_bid(1, illegal_bid=2, total_cards=5)
    assert not validate_bid(2, illegal_bid=2, total_cards=5)
    assert not validate_bid(-1, illegal_bid=None, total_cards=5)
    assert not validate_bid(6, illegal_bid=None, total_cards=5)
