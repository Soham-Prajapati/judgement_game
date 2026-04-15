from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.connection_manager import manager
from services import room_service, game_service
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
    
    # Broadcast current state to all in room
    players = await room_service.redis_client.lrange(f"room:{room_code}:players", 0, -1)
    
    # If it's a new player (not just a reconnect), add to Redis
    if username not in players:
        # Check if room is full
        if len(players) >= 6:
            await websocket.send_json({"type": "server_error", "message": "Room is full"})
            await websocket.close()
            manager.disconnect(websocket, room_code, username)
            return
        
        await room_service.redis_client.redis.rpush(f"room:{room_code}:players", username)
        players.append(username)

    room_meta = await room_service.get_room_meta(room_code)
    
    await manager.broadcast({
        "type": "server_room_state",
        "room_code": room_code,
        "players": players,
        "host": room_meta.get("host", players[0])
    }, room_code)

    try:
        while True:
            data = await websocket.receive_text()
            event = json.loads(data)
            
            if event["type"] == "client_start_game":
                # Verify sender is host
                if username == room_meta.get("host"):
                    game_state = await game_service.start_game(room_code)
                    
                    # Broadcast deal to each player (private hands)
                    for p in players:
                        if p in manager.user_connections.get(room_code, {}):
                            p_socket = manager.user_connections[room_code][p]
                            await manager.send_personal_message({
                                "type": "server_deal_cards",
                                "hand": game_state["hands"][p],
                                "trump_suit": game_state["trump_suit"],
                                "round_num": game_state["round_num"],
                                "total_cards": game_state["cards_per_player"]
                            }, p_socket)
                    
                    # Also broadcast bid request for first bidder
                    await manager.broadcast({
                        "type": "server_bid_request",
                        "current_bidder": players[0], # First player always starts for now
                        "bids_so_far": {},
                        "illegal_bid": None # Not last bidder yet
                    }, room_code)
                else:
                    await websocket.send_json({"type": "server_error", "message": "Only host can start game"})

    except WebSocketDisconnect:
        manager.disconnect(websocket, room_code, username)
        # In real app, we'd handle more complex disconnect logic (host migration)
        # but for now just broadcast left
        updated_players = await room_service.redis_client.lrange(f"room:{room_code}:players", 0, -1)
        await manager.broadcast({
            "type": "server_player_left",
            "username": username,
            "players": updated_players
        }, room_code)
    except Exception as e:
        print(f"WS Error: {e}")
        manager.disconnect(websocket, room_code, username)
