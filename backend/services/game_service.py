from .redis_client import redis_client
from game.deck import create_deck, shuffle_deck, deal_cards, Card
from game.trump import get_trump_suit
from game.bidding import is_valid_bid, get_illegal_bid
from game.tricks import is_valid_play, get_trick_winner
from game.scoring import calculate_round_score
import json
import os

ROOM_TTL = int(os.getenv("ROOM_TTL_SECONDS", 7200))
MAX_CARDS_IN_PEAK = 7 # The "top" of the U-Turn

async def get_cards_for_round(round_num: int) -> int:
    """
    Calculates cards to deal based on U-Turn logic:
    1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1
    """
    if round_num <= MAX_CARDS_IN_PEAK:
        return round_num
    else:
        # After peak, decrease. 
        # e.g. round 8 returns 6, round 9 returns 5...
        diff = round_num - MAX_CARDS_IN_PEAK
        val = MAX_CARDS_IN_PEAK - diff
        return max(val, 1)

async def start_game(room_code: str, round_num: int = 1):
    players = await redis_client.lrange(f"room:{room_code}:players", 0, -1)
    num_players = len(players)
    
    cards_per_player = await get_cards_for_round(round_num)
    
    # Safety check: 52 cards total. 8 players * 6 cards = 48.
    # If 8 players, we can't do 7 cards (56).
    if num_players * cards_per_player > 52:
        cards_per_player = 52 // num_players

    deck = create_deck()
    shuffle_deck(deck)
    hands, _ = deal_cards(deck, num_players, cards_per_player)
    trump_suit = get_trump_suit(round_num)
    
    hands_dict = {u: json.dumps([c.to_dict() for c in hands[i]]) for i, u in enumerate(players)}
    await redis_client.hset(f"room:{room_code}:hands", mapping=hands_dict)
    await redis_client.redis.expire(f"room:{room_code}:hands", ROOM_TTL)
    
    await redis_client.delete(f"room:{room_code}:bids")
    await redis_client.delete(f"room:{room_code}:tricks_won")
    await redis_client.delete(f"room:{room_code}:trick_pile")
    
    await redis_client.hset(f"room:{room_code}:meta", mapping={
        "status": "bidding",
        "round_num": str(round_num),
        "cards_per_player": str(cards_per_player),
        "trump_suit": trump_suit,
        "current_bidder_idx": "0"
    })
    
    return {
        "round_num": round_num,
        "cards_per_player": cards_per_player,
        "trump_suit": trump_suit,
        "hands": {u: json.loads(h) for u, h in hands_dict.items()},
        "players": players
    }

async def place_bid(room_code: str, username: str, bid: int):
    players = await redis_client.lrange(f"room:{room_code}:players", 0, -1)
    meta = await redis_client.hgetall(f"room:{room_code}:meta")
    cards_per_player = int(meta["cards_per_player"])
    current_bidder_idx = int(meta["current_bidder_idx"])
    
    if players[current_bidder_idx] != username:
        return False, "Not your turn to bid"
    
    bids_raw = await redis_client.hgetall(f"room:{room_code}:bids")
    current_bids = [int(v) for v in bids_raw.values()]
    is_last = (current_bidder_idx == len(players) - 1)
    
    if not is_valid_bid(bid, cards_per_player, current_bids, is_last):
        return False, "Invalid bid"
    
    await redis_client.redis.hset(f"room:{room_code}:bids", username, bid)
    
    if is_last:
        await redis_client.hset(f"room:{room_code}:meta", mapping={
            "status": "playing",
            "current_player_idx": "0" 
        })
        return True, {"type": "playing_transition", "bids": await redis_client.hgetall(f"room:{room_code}:bids")}
    else:
        next_idx = current_bidder_idx + 1
        await redis_client.hset(f"room:{room_code}:meta", "current_bidder_idx", str(next_idx))
        updated_bids = await redis_client.hgetall(f"room:{room_code}:bids")
        next_is_last = (next_idx == len(players) - 1)
        illegal = get_illegal_bid(cards_per_player, [int(v) for v in updated_bids.values()], True) if next_is_last else None
            
        return True, {
            "type": "next_bidder",
            "next_bidder": players[next_idx],
            "bids": updated_bids,
            "illegal_bid": illegal
        }

async def play_card(room_code: str, username: str, card_dict: dict):
    players = await redis_client.lrange(f"room:{room_code}:players", 0, -1)
    meta = await redis_client.hgetall(f"room:{room_code}:meta")
    current_player_idx = int(meta["current_player_idx"])
    
    if players[current_player_idx] != username:
        return False, "Not your turn"
    
    hands_raw = await redis_client.hgetall(f"room:{room_code}:hands")
    hand = [Card(**c) for c in json.loads(hands_raw[username])]
    trick_raw = await redis_client.lrange(f"room:{room_code}:trick_pile", 0, -1)
    trick = [(item.split(":")[0], Card(**json.loads(item.split(":")[1]))) for item in trick_raw]
    
    played_card = Card(**card_dict)
    if not is_valid_play(played_card, hand, trick):
        return False, "Must follow suit"
    
    new_hand = [c for c in hand if not (c.suit == played_card.suit and c.rank == played_card.rank)]
    await redis_client.hset(f"room:{room_code}:hands", username, json.dumps([c.to_dict() for c in new_hand]))
    await redis_client.redis.rpush(f"room:{room_code}:trick_pile", f"{username}:{json.dumps(card_dict)}")
    
    updated_trick_raw = await redis_client.lrange(f"room:{room_code}:trick_pile", 0, -1)
    updated_trick = [json.loads(item.split(":")[1]) for item in updated_trick_raw]
    
    if len(updated_trick) == len(players):
        trick_objects = [(item.split(":")[0], Card(**json.loads(item.split(":")[1]))) for item in updated_trick_raw]
        winner = get_trick_winner(trick_objects, meta["trump_suit"])
        await redis_client.redis.hincrby(f"room:{room_code}:tricks_won", winner, 1)
        winner_idx = players.index(winner)
        await redis_client.hset(f"room:{room_code}:meta", "current_player_idx", str(winner_idx))
        await redis_client.delete(f"room:{room_code}:trick_pile")
        
        if len(new_hand) == 0:
            results = await calculate_round_end(room_code, players)
            return True, {"type": "round_end", "winner": winner, "trick_cards": updated_trick, "round_results": results}
        return True, {"type": "trick_resolved", "winner": winner, "trick_cards": updated_trick}
    else:
        next_player_idx = (current_player_idx + 1) % len(players)
        await redis_client.hset(f"room:{room_code}:meta", "current_player_idx", str(next_player_idx))
        return True, {
            "type": "card_played", "player": username, "card": card_dict,
            "next_player": players[next_player_idx], "trick_so_far": updated_trick
        }

async def calculate_round_end(room_code: str, players: list):
    bids = await redis_client.hgetall(f"room:{room_code}:bids")
    tricks_won = await redis_client.hgetall(f"room:{room_code}:tricks_won")
    round_scores = {}
    for p in players:
        p_bid, p_won = int(bids.get(p, 0)), int(tricks_won.get(p, 0))
        score = calculate_round_score(p_bid, p_won)
        round_scores[p] = score
        await redis_client.redis.hincrby(f"room:{room_code}:total_scores", p, score)
    
    total_scores = await redis_client.hgetall(f"room:{room_code}:total_scores")
    meta = await redis_client.hgetall(f"room:{room_code}:meta")
    round_num = int(meta["round_num"])
    await redis_client.hset(f"room:{room_code}:history:{round_num}", mapping=round_scores)
    
    # Game Over if we finished the "down" part of the U-Turn
    # If peak is 7, total rounds = 13
    if round_num >= (MAX_CARDS_IN_PEAK * 2 - 1):
        await redis_client.hset(f"room:{room_code}:meta", "status", "game_over")
        winner = max(total_scores, key=lambda k: int(total_scores[k]))
        return {"round_num": round_num, "round_scores": round_scores, "total_scores": total_scores, "game_over": True, "winner": winner}
    
    await redis_client.hset(f"room:{room_code}:meta", "status", "round_end")
    return {"round_num": round_num, "round_scores": round_scores, "total_scores": total_scores, "game_over": False}

async def start_next_round(room_code: str):
    meta = await redis_client.hgetall(f"room:{room_code}:meta")
    round_num = int(meta["round_num"]) + 1
    return await start_game(room_code, round_num)

async def reset_game(room_code: str):
    await redis_client.delete(f"room:{room_code}:total_scores")
    for i in range(1, 20): await redis_client.delete(f"room:{room_code}:history:{i}")
    return await start_game(room_code, 1)
