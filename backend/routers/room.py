from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services import room_service
from services.redis_client import redis_client

router = APIRouter(prefix="/room", tags=["room"])

class CreateRoomRequest(BaseModel):
    username: str

class CreateRoomResponse(BaseModel):
    room_code: str

class RoomExistsResponse(BaseModel):
    exists: bool
    player_count: int

@router.post("/create", response_model=CreateRoomResponse)
async def create_room(request: CreateRoomRequest):
    try:
        await redis_client.connect()
        room_code = await room_service.create_room(request.username)
        return CreateRoomResponse(room_code=room_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{code}/exists", response_model=RoomExistsResponse)
async def check_room_exists(code: str):
    try:
        await redis_client.connect()
        exists = await room_service.room_exists(code)
        player_count = 0
        if exists:
            player_count = await room_service.get_player_count(code)
        return RoomExistsResponse(exists=exists, player_count=player_count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
