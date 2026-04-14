from __future__ import annotations

import os
from dataclasses import dataclass, field

from game.bidding import get_illegal_bid, validate_bid
from game.deck import create_deck, deal_cards, shuffle_deck
from game.scoring import calculate_round_scores, update_cumulative_scores
from game.tricks import determine_trick_winner, get_playable_cards
from game.trump import get_trump_for_round

DEFAULT_START_CARDS = int(os.getenv("DEFAULT_START_CARDS", "7"))


@dataclass
class GameState:
    room_code: str
    players: list[str]
    host: str
    status: str = "lobby"
    round_num: int = 0
    round_sequence: list[int] = field(default_factory=list)
    dealer_index: int = 0
    total_cards: int = 0
    trump_suit: str = ""
    hands: dict[str, list[dict[str, str]]] = field(default_factory=dict)
    bid_order: list[str] = field(default_factory=list)
    bids: dict[str, int] = field(default_factory=dict)
    bid_turn_index: int = 0
    tricks_won: dict[str, int] = field(default_factory=dict)
    current_player: str = ""
    current_trick: list[dict[str, dict[str, str] | str]] = field(default_factory=list)
    lead_suit: str | None = None
    scores: dict[str, list[int]] = field(default_factory=dict)
    disconnected: set[str] = field(default_factory=set)


class GameService:
    def __init__(self) -> None:
        self._games: dict[str, GameState] = {}

    def get_state(self, room_code: str) -> GameState | None:
        return self._games.get(room_code.upper())

    def ensure_room(self, room_code: str, players: list[str], host: str) -> GameState:
        key = room_code.upper()
        existing = self._games.get(key)
        if existing is None:
            state = GameState(room_code=key, players=players.copy(), host=host)
            self._games[key] = state
            return state

        existing.players = players.copy()
        existing.host = host
        existing.disconnected = {name for name in existing.disconnected if name in existing.players}
        for player in existing.players:
            existing.scores.setdefault(player, [])
        return existing

    def remove_player(self, room_code: str, username: str) -> dict[str, str | bool]:
        key = room_code.upper()
        state = self._games.get(key)
        if state is None:
            return {"skipped": True}

        if state.status == "lobby":
            state.players = [name for name in state.players if name != username]
            state.scores.pop(username, None)
            if not state.players:
                self._games.pop(key, None)
                return {"room_deleted": True}
            state.host = state.players[0] if state.host == username else state.host
            return {"new_host": state.host}

        state.disconnected.add(username)
        if state.current_player == username:
            state.current_player = self._next_connected_player(state, username)
        if state.host == username:
            connected = [name for name in state.players if name not in state.disconnected]
            if connected:
                state.host = connected[0]
                return {"new_host": state.host, "skipped": True}
        return {"skipped": True}

    def delete_room(self, room_code: str) -> None:
        self._games.pop(room_code.upper(), None)

    def start_game(self, room_code: str, players: list[str], host: str) -> dict:
        if len(players) < 2:
            raise ValueError("not_enough_players")

        state = self.ensure_room(room_code, players, host)
        max_cards = max(1, min(DEFAULT_START_CARDS, 52 // len(players)))
        state.round_sequence = list(range(max_cards, 0, -1))
        state.round_num = 0
        state.dealer_index = 0
        state.disconnected = set()
        state.scores = {player: [] for player in players}
        return self._start_next_round(state)

    def next_round(self, room_code: str, username: str) -> dict:
        state = self._require_state(room_code)
        if username != state.host:
            raise ValueError("host_only")
        if state.status != "round_end":
            raise ValueError("invalid_phase")
        return self._start_next_round(state)

    def rematch(self, room_code: str, username: str) -> dict:
        state = self._require_state(room_code)
        if username != state.host:
            raise ValueError("host_only")
        players = [name for name in state.players if name not in state.disconnected]
        if len(players) < 2:
            raise ValueError("not_enough_players")
        return self.start_game(room_code, players, state.host)

    def place_bid(self, room_code: str, username: str, bid: int) -> dict:
        state = self._require_state(room_code)
        if state.status != "bidding":
            raise ValueError("invalid_phase")
        if state.bid_order[state.bid_turn_index] != username:
            raise ValueError("not_your_turn")

        illegal_bid = get_illegal_bid(
            current_bids=state.bids,
            total_cards=state.total_cards,
            is_last_bidder=state.bid_turn_index == len(state.bid_order) - 1,
        )
        if not validate_bid(bid, illegal_bid=illegal_bid, total_cards=state.total_cards):
            raise ValueError("invalid_bid")

        state.bids[username] = bid
        state.bid_turn_index += 1

        # Disconnected players are auto-skipped with a safe default bid.
        while state.bid_turn_index < len(state.bid_order):
            candidate = state.bid_order[state.bid_turn_index]
            if candidate not in state.disconnected:
                break
            state.bids[candidate] = 0
            state.bid_turn_index += 1

        response: dict[str, dict | list[dict[str, str]]] = {
            "server_bid_update": {"type": "server_bid_update", "bids": state.bids.copy()}
        }

        if state.bid_turn_index < len(state.bid_order):
            next_bidder = state.bid_order[state.bid_turn_index]
            response["server_bid_request"] = {
                "type": "server_bid_request",
                "current_bidder": next_bidder,
                "bids_so_far": state.bids.copy(),
                "illegal_bid": get_illegal_bid(
                    current_bids=state.bids,
                    total_cards=state.total_cards,
                    is_last_bidder=state.bid_turn_index == len(state.bid_order) - 1,
                ),
            }
            return response

        state.status = "playing"
        first_player = self._next_connected_player(state, state.bid_order[0], include_current=True)
        state.current_player = first_player
        response["server_turn_update"] = {
            "type": "server_turn_update",
            "current_player": first_player,
            "trick_so_far": [],
        }
        return response

    def play_card(self, room_code: str, username: str, card: dict[str, str]) -> dict:
        state = self._require_state(room_code)
        if state.status != "playing":
            raise ValueError("invalid_phase")
        if state.current_player != username:
            raise ValueError("not_your_turn")
        if username in state.disconnected:
            raise ValueError("player_disconnected")

        hand = state.hands.get(username, [])
        if card not in hand:
            raise ValueError("card_not_in_hand")

        playable = get_playable_cards(hand, state.lead_suit)
        if card not in playable:
            raise ValueError("must_follow_suit")

        hand.remove(card)
        state.current_trick.append({"username": username, "card": card})
        if state.lead_suit is None:
            state.lead_suit = card["suit"]

        connected_players = [name for name in state.players if name not in state.disconnected]
        if len(state.current_trick) < len(connected_players):
            state.current_player = self._next_connected_player(state, username)
            return {
                "server_turn_update": {
                    "type": "server_turn_update",
                    "current_player": state.current_player,
                    "trick_so_far": state.current_trick.copy(),
                }
            }

        winner = determine_trick_winner(
            trick_pile=state.current_trick,
            trump_suit=state.trump_suit,
            lead_suit=state.lead_suit or "",
        )
        state.tricks_won[winner] = state.tricks_won.get(winner, 0) + 1
        trick_cards = state.current_trick.copy()
        state.current_trick = []
        state.lead_suit = None
        state.current_player = winner

        response: dict[str, dict] = {
            "server_trick_result": {
                "type": "server_trick_result",
                "winner": winner,
                "trick_cards": trick_cards,
            }
        }

        # Round end happens when every connected player has no cards left.
        if all(not state.hands[name] for name in connected_players):
            round_scores = calculate_round_scores(state.bids, state.tricks_won)
            state.scores = update_cumulative_scores(state.scores, round_scores)

            if state.round_num >= len(state.round_sequence):
                state.status = "game_over"
                winner_name = max(
                    state.scores,
                    key=lambda player: sum(state.scores[player]),
                )
                response["server_game_over"] = {
                    "type": "server_game_over",
                    "final_scores": state.scores,
                    "winner": winner_name,
                }
                return response

            state.status = "round_end"
            response["server_round_end"] = {
                "type": "server_round_end",
                "scores": round_scores,
                "round_num": state.round_num,
                "cumulative_scores": state.scores,
            }
            return response

        response["server_turn_update"] = {
            "type": "server_turn_update",
            "current_player": state.current_player,
            "trick_so_far": [],
        }
        return response

    def _start_next_round(self, state: GameState) -> dict:
        if state.round_num >= len(state.round_sequence):
            raise ValueError("game_complete")

        state.round_num += 1
        state.status = "bidding"
        state.total_cards = state.round_sequence[state.round_num - 1]
        state.trump_suit = get_trump_for_round(state.round_num)
        state.bids = {}
        state.bid_turn_index = 0
        state.tricks_won = {player: 0 for player in state.players}
        state.current_trick = []
        state.lead_suit = None

        # Dealer rotates each round; bidding starts with the player to the left.
        state.dealer_index = (state.round_num - 1) % len(state.players)
        bid_start_index = (state.dealer_index + 1) % len(state.players)
        state.bid_order = state.players[bid_start_index:] + state.players[:bid_start_index]

        shuffled = shuffle_deck(create_deck())
        state.hands = deal_cards(shuffled, state.players, state.total_cards)
        for player in state.players:
            state.scores.setdefault(player, [])

        current_bidder = self._next_connected_player(state, state.bid_order[0], include_current=True)
        state.bid_turn_index = state.bid_order.index(current_bidder)

        return {
            "deals": {
                player: {
                    "type": "server_deal_cards",
                    "hand": hand,
                    "trump_suit": state.trump_suit,
                    "round_num": state.round_num,
                    "total_cards": state.total_cards,
                }
                for player, hand in state.hands.items()
                if player not in state.disconnected
            },
            "server_bid_request": {
                "type": "server_bid_request",
                "current_bidder": current_bidder,
                "bids_so_far": {},
                "illegal_bid": None,
            },
        }

    def _next_connected_player(
        self,
        state: GameState,
        from_player: str,
        include_current: bool = False,
    ) -> str:
        if not state.players:
            raise ValueError("no_players")

        start = state.players.index(from_player) if from_player in state.players else 0
        steps = range(0 if include_current else 1, len(state.players) + 1)
        for offset in steps:
            candidate = state.players[(start + offset) % len(state.players)]
            if candidate not in state.disconnected:
                return candidate
        raise ValueError("no_connected_players")

    def _require_state(self, room_code: str) -> GameState:
        state = self._games.get(room_code.upper())
        if state is None:
            raise ValueError("room_not_initialized")
        return state


game_service = GameService()