from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from services.connection_manager import ConnectionManager
from services.game_service import game_service
from services import room_service

router = APIRouter()
manager = ConnectionManager()


async def _send_error(websocket: WebSocket, code: str, message: str) -> None:
    await websocket.send_json({"type": "server_error", "code": code, "message": message})


@router.websocket("/ws/{room_code}/{username}")
async def websocket_endpoint(websocket: WebSocket, room_code: str, username: str) -> None:
    normalized_room_code = room_code.upper()

    try:
        snapshot = await room_service.add_player(normalized_room_code, username)
    except ValueError as exc:
        await websocket.accept()
        await _send_error(websocket, str(exc), "Unable to join room")
        await websocket.close(code=1008)
        return
    except Exception:
        await websocket.accept()
        await _send_error(websocket, "room_service_unavailable", "Room service unavailable")
        await websocket.close(code=1011)
        return

    await manager.connect(normalized_room_code, username, websocket)
    game_service.ensure_room(normalized_room_code, snapshot.players, snapshot.host)

    await manager.broadcast_to_room(
        normalized_room_code,
        {
            "type": "server_room_state",
            "room_code": normalized_room_code,
            "host": snapshot.host,
            "players": snapshot.players,
        },
    )

    try:
        while True:
            payload = await websocket.receive_json()
            event_type = payload.get("type")
            if event_type == "ping":
                await manager.send_to_player(normalized_room_code, username, {"type": "pong"})
                continue

            if event_type == "client_start_game":
                snapshot = await room_service.get_snapshot(normalized_room_code)
                if snapshot is None:
                    await _send_error(websocket, "room_not_found", "Room does not exist")
                    continue
                if username != snapshot.host:
                    await _send_error(websocket, "host_only", "Only host can start game")
                    continue

                result = game_service.start_game(normalized_room_code, snapshot.players, snapshot.host)
                await room_service.update_room_status(normalized_room_code, "bidding")

                for player, deal_payload in result["deals"].items():
                    await manager.send_to_player(normalized_room_code, player, deal_payload)

                await manager.broadcast_to_room(normalized_room_code, result["server_bid_request"])
                continue

            if event_type == "client_place_bid":
                try:
                    bid = int(payload.get("bid"))
                except (TypeError, ValueError):
                    await _send_error(websocket, "invalid_bid", "Bid must be a number")
                    continue

                try:
                    result = game_service.place_bid(normalized_room_code, username, bid)
                except ValueError as exc:
                    await _send_error(websocket, str(exc), "Bid rejected")
                    continue

                await manager.broadcast_to_room(normalized_room_code, result["server_bid_update"])
                if "server_bid_request" in result:
                    await manager.broadcast_to_room(normalized_room_code, result["server_bid_request"])
                if "server_turn_update" in result:
                    await room_service.update_room_status(normalized_room_code, "playing")
                    await manager.broadcast_to_room(normalized_room_code, result["server_turn_update"])
                continue

            if event_type == "client_play_card":
                card = payload.get("card")
                if not isinstance(card, dict) or "suit" not in card or "value" not in card:
                    await _send_error(websocket, "invalid_card", "Card payload is invalid")
                    continue

                try:
                    result = game_service.play_card(normalized_room_code, username, card)
                except ValueError as exc:
                    await _send_error(websocket, str(exc), "Card play rejected")
                    continue

                if "server_turn_update" in result:
                    await manager.broadcast_to_room(normalized_room_code, result["server_turn_update"])
                if "server_trick_result" in result:
                    await manager.broadcast_to_room(normalized_room_code, result["server_trick_result"])
                if "server_round_end" in result:
                    await room_service.update_room_status(normalized_room_code, "round_end")
                    await manager.broadcast_to_room(normalized_room_code, result["server_round_end"])
                if "server_game_over" in result:
                    await room_service.update_room_status(normalized_room_code, "game_over")
                    await manager.broadcast_to_room(normalized_room_code, result["server_game_over"])
                continue

            if event_type == "client_next_round":
                try:
                    result = game_service.next_round(normalized_room_code, username)
                except ValueError as exc:
                    await _send_error(websocket, str(exc), "Cannot advance round")
                    continue

                await room_service.update_room_status(normalized_room_code, "bidding")
                for player, deal_payload in result["deals"].items():
                    await manager.send_to_player(normalized_room_code, player, deal_payload)
                await manager.broadcast_to_room(normalized_room_code, result["server_bid_request"])
                continue

            if event_type == "client_rematch":
                try:
                    result = game_service.rematch(normalized_room_code, username)
                except ValueError as exc:
                    await _send_error(websocket, str(exc), "Cannot start rematch")
                    continue

                await room_service.update_room_status(normalized_room_code, "bidding")
                for player, deal_payload in result["deals"].items():
                    await manager.send_to_player(normalized_room_code, player, deal_payload)
                await manager.broadcast_to_room(normalized_room_code, result["server_bid_request"])
                continue

            await _send_error(websocket, "unsupported_event", "Unsupported event type")
    except WebSocketDisconnect:
        await manager.disconnect(normalized_room_code, username)

        snapshot, migrated_host = await room_service.remove_player(normalized_room_code, username)
        game_update = game_service.remove_player(normalized_room_code, username)

        new_host = migrated_host or game_update.get("new_host")
        await manager.broadcast_to_room(
            normalized_room_code,
            {
                "type": "server_player_left",
                "username": username,
                "new_host": new_host,
            },
        )

        if snapshot is None:
            game_service.delete_room(normalized_room_code)
            return

        current_state = game_service.get_state(normalized_room_code)
        if current_state is None or current_state.status == "lobby":
            game_service.ensure_room(normalized_room_code, snapshot.players, snapshot.host)
        await manager.broadcast_to_room(
            normalized_room_code,
            {
                "type": "server_room_state",
                "room_code": normalized_room_code,
                "host": snapshot.host,
                "players": snapshot.players,
            },
        )
