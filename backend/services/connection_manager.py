from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # room_code -> [WebSocket]
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # room_code -> {username: WebSocket}
        self.user_connections: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_code: str, username: str):
        await websocket.accept()
        
        if room_code not in self.active_connections:
            self.active_connections[room_code] = []
        self.active_connections[room_code].append(websocket)
        
        if room_code not in self.user_connections:
            self.user_connections[room_code] = {}
        self.user_connections[room_code][username] = websocket

    def disconnect(self, websocket: WebSocket, room_code: str, username: str):
        if room_code in self.active_connections:
            self.active_connections[room_code].remove(websocket)
        
        if room_code in self.user_connections:
            if username in self.user_connections[room_code]:
                del self.user_connections[room_code][username]

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: dict, room_code: str):
        if room_code in self.active_connections:
            for connection in self.active_connections[room_code]:
                await connection.send_json(message)

manager = ConnectionManager()
