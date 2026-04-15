from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.connection_manager import manager
from services import room_service
import json

router = APIRouter(tags=["websocket"])

@router.websocket("/ws/{room_code}/{username}")
async def websocket_endpoint(websocket: WebSocket, room_code: str, username: str):
    # Check if room exists
    if not await room_service.room_exists(room_code):
        await websocket.accept()
        await websocket.send_json({"type": "server_error", "message": "Room not found"})
        await websocket.close()
        return

    await manager.connect(websocket, room_code, username)
    
    # Broadcast join message
    players = await room_service.lrange(f"room:{room_code}:players", 0, -1)
    if username not in players:
        # This handles reconnect vs new join
        # In a real app we'd add to Redis list here if not already there
        pass

    await manager.broadcast({
        "type": "server_room_state",
        "room_code": room_code,
        "players": players,
        # In a real implementation we'd fetch the actual host from Redis
        "host": players[-1] if players else username 
    }, room_code)

    try:
        while True:
            data = await websocket.receive_text()
            event = json.loads(data)
            
            # Handle events based on type
            # client_place_bid, client_play_card, etc.
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_code, username)
        # Handle disconnect (host promotion, auto-skip, etc.)
        players = await room_service.lrange(f"room:{room_code}:players", 0, -1)
        await manager.broadcast({
            "type": "server_player_left",
            "username": username,
            "players": players
        }, room_code)
