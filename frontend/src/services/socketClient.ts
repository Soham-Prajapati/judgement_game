import { AppConstants } from '../core/constants';
import { useRoomStore } from '../store/useRoomStore';
import { useGameStore } from '../store/useGameStore';

class SocketClient {
  private socket: WebSocket | null = null;
  private roomCode: string | null = null;
  private username: string | null = null;

  connect(roomCode: string, username: string) {
    this.roomCode = roomCode;
    this.username = username;
    const url = `${AppConstants.wsBaseUrl}/ws/${roomCode}/${username}`;
    
    this.socket = new WebSocket(url);

    this.socket.onopen = () => {
      console.log('WS Connected');
    };

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handleMessage(data);
    };

    this.socket.onclose = () => {
      console.log('WS Closed');
    };

    this.socket.onerror = (error) => {
      console.error('WS Error:', error);
    };
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }

  send(type: string, payload: any = {}) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ type, ...payload }));
    }
  }

  private handleMessage(data: any) {
    const gameStore = useGameStore.getState();
    const roomStore = useRoomStore.getState();

    switch (data.type) {
      case 'server_room_state':
        roomStore.setRoom(data.room_code, data.players, data.host);
        break;
      
      case 'server_deal_cards':
        gameStore.setHand(data.hand);
        gameStore.setRoundInfo(data.round_num, data.trump_suit);
        gameStore.setStatus('bidding');
        break;
      
      case 'server_bid_request':
        gameStore.setBidRequest(data.current_bidder, data.illegal_bid);
        break;
      
      case 'server_bid_update':
        gameStore.setBids(data.bids);
        break;
      
      case 'server_turn_update':
        gameStore.setTurnUpdate(data.current_player, data.trick_so_far);
        break;
      
      case 'server_trick_result':
        gameStore.setTrickResult(data.winner, data.trick_cards);
        break;
      
      case 'server_round_end':
        gameStore.setRoundEnd(data.round_num, data.scores, data.total_scores, false);
        break;
      
      case 'server_game_over':
        gameStore.setRoundEnd(0, {}, data.final_scores, true, data.winner);
        break;
      
      case 'server_player_left':
        roomStore.updatePlayers(data.players);
        break;
      
      case 'server_error':
        console.error('Server Error:', data.message);
        break;
    }
  }
}

export const socketClient = new SocketClient();
