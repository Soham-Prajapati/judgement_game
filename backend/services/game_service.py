from .redis_client import redis_client
from game.deck import create_deck, shuffle_deck, deal_cards
from game.trump import get_trump_suit
import json
import os

ROOM_TTL = int(os.getenv("ROOM_TTL_SECONDS", 7200))

async def start_game(room_code: str):
    """
    Initializes a new game for a room.
    1. Sets round to 1
    2. Determines cards to deal (default 7 for round 1)
    3. Deals cards
    4. Saves hands and trump to Redis
    5. Updates room status to 'bidding'
    """
    players = await redis_client.lrange(f"room:{room_code}:players", 0, -1)
    num_players = len(players)
    round_num = 1
    cards_per_player = 7 # Default start
    
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
    
    # Update room meta
    await redis_client.hset(f"room:{room_code}:meta", {
        "status": "bidding",
        "round_num": str(round_num),
        "cards_per_player": str(cards_per_player),
        "trump_suit": trump_suit,
        "current_bidder_idx": "0" # First player after dealer (simplification: index 0)
    })
    
    return {
        "round_num": round_num,
        "cards_per_player": cards_per_player,
        "trump_suit": trump_suit,
        "hands": {u: json.loads(h) for u, h in hands_dict.items()},
        "players": players
    }
