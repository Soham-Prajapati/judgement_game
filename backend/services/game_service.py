from .redis_client import redis_client
from game.deck import create_deck, shuffle_deck, deal_cards
from game.trump import get_trump_suit
from game.bidding import is_valid_bid, get_illegal_bid
import json
import os

ROOM_TTL = int(os.getenv("ROOM_TTL_SECONDS", 7200))

async def start_game(room_code: str):
    """
    Initializes a new game for a room.
    """
    players = await redis_client.lrange(f"room:{room_code}:players", 0, -1)
    num_players = len(players)
    round_num = 1
    cards_per_player = 7 
    
    deck = create_deck()
    shuffle_deck(deck)
    
    hands, _ = deal_cards(deck, num_players, cards_per_player)
    trump_suit = get_trump_suit(round_num)
    
    # Store hands in Redis: room:{code}:hands -> {username: [cards]}
    hands_dict = {}
    for i, username in enumerate(players):
        hands_dict[username] = json.dumps([c.to_dict() for c in hands[i]])
    
    await redis_client.hset(f"room:{room_code}:hands", hands_dict)
    await redis_client.redis.expire(f"room:{room_code}:hands", ROOM_TTL)
    
    # Clear previous bids
    await redis_client.delete(f"room:{room_code}:bids")
    
    # Update room meta
    await redis_client.hset(f"room:{room_code}:meta", {
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
    """
    Handles a player placing a bid.
    Returns: (success, next_state)
    """
    players = await redis_client.lrange(f"room:{room_code}:players", 0, -1)
    meta = await redis_client.hgetall(f"room:{room_code}:meta")
    
    cards_per_player = int(meta["cards_per_player"])
    current_bidder_idx = int(meta["current_bidder_idx"])
    
    # Verify it's this player's turn
    if players[current_bidder_idx] != username:
        return False, "Not your turn to bid"
    
    # Get current bids
    bids_raw = await redis_client.hgetall(f"room:{room_code}:bids")
    current_bids = [int(v) for v in bids_raw.values()]
    
    is_last = (current_bidder_idx == len(players) - 1)
    
    if not is_valid_bid(bid, cards_per_player, current_bids, is_last):
        return False, "Invalid bid"
    
    # Save bid
    await redis_client.redis.hset(f"room:{room_code}:bids", username, bid)
    await redis_client.redis.expire(f"room:{room_code}:bids", ROOM_TTL)
    
    # Check if bidding phase is over
    if is_last:
        # All players have bid. Transition to 'playing'
        await redis_client.hset(f"room:{room_code}:meta", {
            "status": "playing",
            "current_player_idx": "0" # First player starts trick 1
        })
        
        # Initialize trick state
        await redis_client.delete(f"room:{room_code}:trick_pile")
        
        return True, {
            "type": "playing_transition",
            "bids": await redis_client.hgetall(f"room:{room_code}:bids")
        }
    else:
        # Next bidder
        next_idx = current_bidder_idx + 1
        await redis_client.hset(f"room:{room_code}:meta", "current_bidder_idx", str(next_idx))
        
        updated_bids = await redis_client.hgetall(f"room:{room_code}:bids")
        
        # Calculate illegal bid for next player if they are last
        next_is_last = (next_idx == len(players) - 1)
        illegal = None
        if next_is_last:
            next_bids = [int(v) for v in updated_bids.values()]
            illegal = get_illegal_bid(cards_per_player, next_bids, True)
            
        return True, {
            "type": "next_bidder",
            "next_bidder": players[next_idx],
            "bids": updated_bids,
            "illegal_bid": illegal
        }
