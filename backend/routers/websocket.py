from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from services.connection_manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()


@router.websocket("/ws/{room_code}/{username}")
async def websocket_endpoint(websocket: WebSocket, room_code: str, username: str) -> None:
    await manager.connect(room_code, username, websocket)
    await manager.send_to_player(
        room_code,
        username,
        {
            "type": "server_room_state",
            "room_code": room_code,
            "host": username,
            "players": list(manager.active_connections.get(room_code, {}).keys()),
        },
    )

    try:
        while True:
            payload = await websocket.receive_json()
            event_type = payload.get("type")
            if event_type == "ping":
                await manager.send_to_player(room_code, username, {"type": "pong"})
            else:
                await manager.broadcast_to_room(
                    room_code,
                    {
                        "type": "server_event_echo",
                        "username": username,
                        "payload": payload,
                    },
                )
    except WebSocketDisconnect:
        await manager.disconnect(room_code, username)
        await manager.broadcast_to_room(
            room_code,
            {"type": "server_player_left", "username": username},
        )
