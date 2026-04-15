import secrets
import string
import os
from .redis_client import redis_client

ROOM_TTL = int(os.getenv("ROOM_TTL_SECONDS", 7200))
CODE_CHARS = string.ascii_uppercase + string.digits

async def generate_room_code() -> str:
    """
    Generates a unique 6-character room code.
    """
    while True:
        code = ''.join(secrets.choice(CODE_CHARS) for _ in range(6))
        # Check if code already exists
        exists = await redis_client.exists(f"room:{code}:meta")
        if not exists:
            return code

async def create_room(host_username: str) -> str:
    """
    Creates a new room in Redis and returns the room code.
    """
    code = await generate_room_code()
    room_key = f"room:{code}:meta"
    
    # Initialize room metadata
    await redis_client.hset(room_key, {
        "code": code,
        "host": host_username,
        "status": "lobby", # lobby, bidding, playing, ended
        "created_at": str(secrets.token_hex(4)) # placeholder for timestamp if needed
    })
    
    # Set TTL for the room
    await redis_client.redis.expire(room_key, ROOM_TTL)
    
    # Also add host to players list
    # Use lpush but we want order preserved, so maybe rpush or just lrange carefully
    await redis_client.redis.rpush(f"room:{code}:players", host_username)
    await redis_client.redis.expire(f"room:{code}:players", ROOM_TTL)

    return code

async def room_exists(code: str) -> bool:
    """
    Checks if a room exists.
    """
    return await redis_client.exists(f"room:{code}:meta")

async def get_player_count(code: str) -> int:
    """
    Returns the number of players in a room.
    """
    players = await redis_client.lrange(f"room:{code}:players", 0, -1)
    return len(players)

async def get_room_meta(code: str) -> dict:
    """
    Returns room metadata.
    """
    return await redis_client.hgetall(f"room:{code}:meta")
