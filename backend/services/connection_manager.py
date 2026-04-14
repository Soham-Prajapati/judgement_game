from __future__ import annotations

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[str, dict[str, WebSocket]] = {}

    async def connect(self, room_code: str, username: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.setdefault(room_code, {})[username] = websocket

    async def disconnect(self, room_code: str, username: str) -> None:
        room_connections = self.active_connections.get(room_code)
        if not room_connections:
            return
        room_connections.pop(username, None)
        if not room_connections:
            self.active_connections.pop(room_code, None)

    async def broadcast_to_room(self, room_code: str, message: dict) -> None:
        for websocket in self.active_connections.get(room_code, {}).values():
            await websocket.send_json(message)

    async def send_to_player(self, room_code: str, username: str, message: dict) -> None:
        websocket = self.active_connections.get(room_code, {}).get(username)
        if websocket is not None:
            await websocket.send_json(message)
