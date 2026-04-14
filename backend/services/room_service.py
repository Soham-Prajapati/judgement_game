from __future__ import annotations

import os
import secrets
import string

from redis.asyncio import Redis

from services.redis_client import get_redis

ROOM_CODE_LENGTH = 6
ROOM_TTL_SECONDS = int(os.getenv("ROOM_TTL_SECONDS", "7200"))
MAX_PLAYERS_PER_ROOM = int(os.getenv("MAX_PLAYERS_PER_ROOM", "6"))


def _generate_room_code() -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(ROOM_CODE_LENGTH))


async def _create_unique_room_code(redis_client: Redis, retries: int = 20) -> str:
    for _ in range(retries):
        code = _generate_room_code()
        exists = await redis_client.exists(f"room:{code}:meta")
        if not exists:
            return code
    raise RuntimeError("Unable to allocate unique room code")


async def create_room() -> str:
    redis_client = get_redis()
    room_code = await _create_unique_room_code(redis_client)
    meta_key = f"room:{room_code}:meta"
    players_key = f"room:{room_code}:players"

    await redis_client.hset(
        meta_key,
        mapping={
            "host": "",
            "status": "lobby",
            "round_num": 0,
            "total_cards": 0,
            "max_players": MAX_PLAYERS_PER_ROOM,
        },
    )
    await redis_client.delete(players_key)
    await redis_client.expire(meta_key, ROOM_TTL_SECONDS)
    await redis_client.expire(players_key, ROOM_TTL_SECONDS)
    return room_code


async def room_exists(room_code: str) -> tuple[bool, int]:
    normalized = room_code.upper()
    redis_client = get_redis()
    meta_key = f"room:{normalized}:meta"
    players_key = f"room:{normalized}:players"

    exists = bool(await redis_client.exists(meta_key))
    if not exists:
        return False, 0

    player_count = int(await redis_client.llen(players_key))
    await redis_client.expire(meta_key, ROOM_TTL_SECONDS)
    await redis_client.expire(players_key, ROOM_TTL_SECONDS)
    return True, player_count
