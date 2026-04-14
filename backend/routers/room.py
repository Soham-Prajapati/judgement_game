from fastapi import APIRouter, HTTPException

from services import room_service

router = APIRouter()


@router.post("/create")
async def create_room() -> dict[str, str]:
    try:
        room_code = await room_service.create_room()
        return {"room_code": room_code}
    except Exception as exc:  # pragma: no cover - depends on infra
        raise HTTPException(status_code=503, detail="Room service unavailable") from exc


@router.get("/{room_code}/exists")
async def room_exists(room_code: str) -> dict[str, int | bool]:
    try:
        exists, player_count = await room_service.room_exists(room_code)
        return {"exists": exists, "player_count": player_count}
    except Exception as exc:  # pragma: no cover - depends on infra
        raise HTTPException(status_code=503, detail="Room service unavailable") from exc
