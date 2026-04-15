from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.connection_manager import manager
from services import room_service, game_service
import json

router = APIRouter(tags=["websocket"])

async def broadcast_deal(room_code: str, players: list, game_state: dict):
    """
    Helper to broadcast private deals to each player.
    """
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

@router.websocket("/ws/{room_code}/{username}")
async def websocket_endpoint(websocket: WebSocket, room_code: str, username: str):
    if not await room_service.room_exists(room_code):
        await websocket.accept()
        await websocket.send_json({"type": "server_error", "message": "Room not found"})
        await websocket.close()
        return

    await manager.connect(websocket, room_code, username)
    players = await room_service.redis_client.lrange(f"room:{room_code}:players", 0, -1)
    
    if username not in players:
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
            room_meta = await room_service.get_room_meta(room_code)
            players = await room_service.redis_client.lrange(f"room:{room_code}:players", 0, -1)

            if event["type"] in ["client_start_game", "client_next_round", "client_rematch"]:
                if username == room_meta.get("host"):
                    if event["type"] == "client_start_game":
                        game_state = await game_service.start_game(room_code)
                    elif event["type"] == "client_next_round":
                        game_state = await game_service.start_next_round(room_code)
                    elif event["type"] == "client_rematch":
                        game_state = await game_service.reset_game(room_code)
                    
                    await broadcast_deal(room_code, players, game_state)
                    await manager.broadcast({
                        "type": "server_bid_request",
                        "current_bidder": players[0],
                        "bids_so_far": {},
                        "illegal_bid": None
                    }, room_code)
                else:
                    await websocket.send_json({"type": "server_error", "message": "Only host can perform this action"})

            elif event["type"] == "client_place_bid":
                bid = event.get("bid")
                success, result = await game_service.place_bid(room_code, username, bid)
                if success:
                    await manager.broadcast({"type": "server_bid_update", "bids": result["bids"]}, room_code)
                    if result["type"] == "next_bidder":
                        await manager.broadcast({
                            "type": "server_bid_request",
                            "current_bidder": result["next_bidder"],
                            "bids_so_far": result["bids"],
                            "illegal_bid": result["illegal_bid"]
                        }, room_code)
                    else:
                        await manager.broadcast({"type": "server_turn_update", "current_player": players[0], "trick_so_far": []}, room_code)
                else:
                    await websocket.send_json({"type": "server_error", "message": result})

            elif event["type"] == "client_play_card":
                card = event.get("card")
                success, result = await game_service.play_card(room_code, username, card)
                if success:
                    if result["type"] == "card_played":
                        await manager.broadcast({"type": "server_turn_update", "current_player": result["next_player"], "trick_so_far": result["trick_so_far"]}, room_code)
                    elif result["type"] == "trick_resolved":
                        await manager.broadcast({"type": "server_trick_result", "winner": result["winner"], "trick_cards": result["trick_cards"]}, room_code)
                        await manager.broadcast({"type": "server_turn_update", "current_player": result["winner"], "trick_so_far": []}, room_code)
                    elif result["type"] == "round_end":
                        await manager.broadcast({"type": "server_trick_result", "winner": result["winner"], "trick_cards": result["trick_cards"]}, room_code)
                        await manager.broadcast({
                            "type": "server_round_end",
                            "round_num": result["round_results"]["round_num"],
                            "scores": result["round_results"]["round_scores"],
                            "total_scores": result["round_results"]["total_scores"]
                        }, room_code)
                        if result["round_results"].get("game_over"):
                            await manager.broadcast({
                                "type": "server_game_over",
                                "final_scores": result["round_results"]["total_scores"],
                                "winner": result["round_results"]["winner"]
                            }, room_code)
                else:
                    await websocket.send_json({"type": "server_error", "message": result})

    except WebSocketDisconnect:
        manager.disconnect(websocket, room_code, username)
        updated_players = await room_service.redis_client.lrange(f"room:{room_code}:players", 0, -1)
        await manager.broadcast({"type": "server_player_left", "username": username, "players": updated_players}, room_code)
    except Exception as e:
        print(f"WS Error: {e}")
        manager.disconnect(websocket, room_code, username)
