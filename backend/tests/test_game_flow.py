from services.game_service import GameService


def test_full_round_completes_to_game_over_for_two_players() -> None:
    service = GameService()
    service.start_game("ROOM01", ["alice", "bob"], "alice")

    state = service.get_state("ROOM01")
    assert state is not None

    # Make the round deterministic and short for integration-style validation.
    state.round_sequence = [1]
    state.total_cards = 1
    state.hands = {
        "alice": [{"suit": "spades", "value": "A"}],
        "bob": [{"suit": "hearts", "value": "2"}],
    }
    state.trump_suit = "spades"

    # Dealer is alice in round 1, so bob bids first.
    first_bid = service.place_bid("ROOM01", "bob", 1)
    assert "server_bid_request" in first_bid

    second_bid = service.place_bid("ROOM01", "alice", 1)
    assert second_bid["server_turn_update"]["current_player"] == "bob"

    turn_update = service.play_card("ROOM01", "bob", {"suit": "hearts", "value": "2"})
    assert turn_update["server_turn_update"]["current_player"] == "alice"

    final_result = service.play_card("ROOM01", "alice", {"suit": "spades", "value": "A"})
    assert "server_trick_result" in final_result
    assert "server_game_over" in final_result
    assert final_result["server_game_over"]["winner"] == "alice"


def test_disconnect_during_game_migrates_host_and_skips_turn() -> None:
    service = GameService()
    service.start_game("ROOM02", ["alice", "bob"], "alice")

    state = service.get_state("ROOM02")
    assert state is not None
    state.status = "playing"
    state.current_player = "alice"

    result = service.remove_player("ROOM02", "alice")

    assert result["new_host"] == "bob"
    assert "alice" in state.disconnected
    assert state.current_player == "bob"


def test_disconnected_bidder_is_auto_skipped() -> None:
    service = GameService()
    service.start_game("ROOM03", ["alice", "bob"], "alice")

    state = service.get_state("ROOM03")
    assert state is not None

    # bob is first bidder in round 1 and disconnects before bidding.
    service.remove_player("ROOM03", "bob")
    response = service.place_bid("ROOM03", "alice", 0)

    assert response["server_bid_update"]["bids"]["bob"] == 0
    assert "server_turn_update" in response