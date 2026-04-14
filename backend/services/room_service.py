from __future__ import annotations

import os
import secrets
import string
from dataclasses import dataclass

from redis.asyncio import Redis

from services.redis_client import get_redis

ROOM_CODE_LENGTH = 6
ROOM_TTL_SECONDS = int(os.getenv("ROOM_TTL_SECONDS", "7200"))
MAX_PLAYERS_PER_ROOM = int(os.getenv("MAX_PLAYERS_PER_ROOM", "6"))


@dataclass
class RoomSnapshot:
    room_code: str
    host: str
    status: str
    players: list[str]

    @property
    def player_count(self) -> int:
        return len(self.players)


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


async def _get_snapshot(redis_client: Redis, room_code: str) -> RoomSnapshot:
    meta_key = f"room:{room_code}:meta"
    players_key = f"room:{room_code}:players"

    meta = await redis_client.hgetall(meta_key)
    players = await redis_client.lrange(players_key, 0, -1)

    return RoomSnapshot(
        room_code=room_code,
        host=meta.get("host", ""),
        status=meta.get("status", "lobby"),
        players=players,
    )


async def add_player(room_code: str, username: str) -> RoomSnapshot:
    normalized_code = room_code.upper()
    cleaned_username = username.strip()
    if not cleaned_username:
        raise ValueError("username_required")

    redis_client = get_redis()
    meta_key = f"room:{normalized_code}:meta"
    players_key = f"room:{normalized_code}:players"

    if not await redis_client.exists(meta_key):
        raise ValueError("room_not_found")

    status = await redis_client.hget(meta_key, "status") or "lobby"
    if status != "lobby":
        raise ValueError("game_already_started")

    players = await redis_client.lrange(players_key, 0, -1)
    if cleaned_username in players:
        raise ValueError("username_taken")
    if len(players) >= MAX_PLAYERS_PER_ROOM:
        raise ValueError("room_full")

    await redis_client.rpush(players_key, cleaned_username)
    current_host = await redis_client.hget(meta_key, "host")
    if not current_host:
        await redis_client.hset(meta_key, mapping={"host": cleaned_username})

    await redis_client.expire(meta_key, ROOM_TTL_SECONDS)
    await redis_client.expire(players_key, ROOM_TTL_SECONDS)
    return await _get_snapshot(redis_client, normalized_code)


async def remove_player(room_code: str, username: str) -> tuple[RoomSnapshot | None, str | None]:
    normalized_code = room_code.upper()
    cleaned_username = username.strip()

    redis_client = get_redis()
    meta_key = f"room:{normalized_code}:meta"
    players_key = f"room:{normalized_code}:players"

    if not await redis_client.exists(meta_key):
        return None, None

    await redis_client.lrem(players_key, 0, cleaned_username)
    players = await redis_client.lrange(players_key, 0, -1)
    host = await redis_client.hget(meta_key, "host") or ""
    new_host: str | None = None

    if host == cleaned_username:
        new_host = players[0] if players else ""
        await redis_client.hset(meta_key, mapping={"host": new_host})

    if not players:
        await delete_room(normalized_code)
        return None, new_host

    await redis_client.expire(meta_key, ROOM_TTL_SECONDS)
    await redis_client.expire(players_key, ROOM_TTL_SECONDS)
    return await _get_snapshot(redis_client, normalized_code), new_host


async def get_snapshot(room_code: str) -> RoomSnapshot | None:
    normalized_code = room_code.upper()
    redis_client = get_redis()
    meta_key = f"room:{normalized_code}:meta"
    if not await redis_client.exists(meta_key):
        return None
    return await _get_snapshot(redis_client, normalized_code)


async def update_room_status(room_code: str, status: str) -> None:
    normalized_code = room_code.upper()
    redis_client = get_redis()
    meta_key = f"room:{normalized_code}:meta"
    players_key = f"room:{normalized_code}:players"

    if await redis_client.exists(meta_key):
        await redis_client.hset(meta_key, mapping={"status": status})
        await redis_client.expire(meta_key, ROOM_TTL_SECONDS)
        await redis_client.expire(players_key, ROOM_TTL_SECONDS)


async def delete_room(room_code: str) -> None:
    normalized_code = room_code.upper()
    redis_client = get_redis()
    keys = [
        f"room:{normalized_code}:meta",
        f"room:{normalized_code}:players",
        f"room:{normalized_code}:hands",
        f"room:{normalized_code}:bids",
        f"room:{normalized_code}:tricks",
        f"room:{normalized_code}:scores",
        f"room:{normalized_code}:trick_pile",
        f"room:{normalized_code}:turn",
        f"room:{normalized_code}:lead_suit",
    ]
    await redis_client.delete(*keys)
