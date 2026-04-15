import secrets
import string
import os
from .redis_client import redis_client

ROOM_TTL = int(os.getenv("ROOM_TTL_SECONDS", 7200))
CODE_CHARS = string.ascii_uppercase + string.digits

async def generate_room_code() -> str:
    while True:
        code = ''.join(secrets.choice(CODE_CHARS) for _ in range(6))
        exists = await redis_client.exists(f"room:{code}:meta")
        if not exists:
            return code

async def create_room(host_username: str) -> str:
    code = await generate_room_code()
    room_key = f"room:{code}:meta"
    await redis_client.hset(room_key, mapping={
        "code": code,
        "host": host_username,
        "status": "lobby",
        "created_at": str(secrets.token_hex(4))
    })
    await redis_client.redis.expire(room_key, ROOM_TTL)
    await redis_client.redis.rpush(f"room:{code}:players", host_username)
    await redis_client.redis.expire(f"room:{code}:players", ROOM_TTL)
    return code

async def room_exists(code: str) -> bool:
    return await redis_client.exists(f"room:{code}:meta")

async def get_player_count(code: str) -> int:
    players = await redis_client.lrange(f"room:{code}:players", 0, -1)
    return len(players)

async def get_room_meta(code: str) -> dict:
    return await redis_client.hgetall(f"room:{code}:meta")

async def remove_player(code: str, username: str):
    """Removes a player from the room's player list."""
    await redis_client.redis.lrem(f"room:{code}:players", 0, username)

async def update_room_meta(code: str, updates: dict):
    """Updates room metadata."""
    await redis_client.hset(f"room:{code}:meta", mapping=updates)

async def delete_room(code: str):
    """Cleans up all room data."""
    await redis_client.delete(f"room:{code}:meta")
    await redis_client.delete(f"room:{code}:players")
    await redis_client.delete(f"room:{code}:hands")
    await redis_client.delete(f"room:{code}:bids")
    await redis_client.delete(f"room:{code}:tricks_won")
    await redis_client.delete(f"room:{code}:total_scores")
    for i in range(1, 8):
        await redis_client.delete(f"room:{code}:history:{i}")
