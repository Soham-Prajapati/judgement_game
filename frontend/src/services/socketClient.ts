import { AppConstants } from '../core/constants';
import { useRoomStore } from '../store/useRoomStore';
import { useGameStore } from '../store/useGameStore';
import { useUserStore } from '../store/useUserStore';

class SocketClient {
  private socket: WebSocket | null = null;
  private roomCode: string | null = null;
  private username: string | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  connect(roomCode: string, username: string) {
    this.roomCode = roomCode;
    this.username = username;
    const url = `${AppConstants.wsBaseUrl}/ws/${roomCode}/${username}`;
    
    console.log('Connecting to:', url);
    this.socket = new WebSocket(url);

    this.socket.onopen = () => {
      console.log('WS Connected');
      this.reconnectAttempts = 0;
    };

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.handleMessage(data);
      } catch (e) {
        console.error('Failed to parse WS message:', e);
      }
    };

    this.socket.onclose = (e) => {
      console.log('WS Closed:', e.code, e.reason);
      this.attemptReconnect();
    };

    this.socket.onerror = (error) => {
      console.error('WS Error:', error);
    };
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts && this.roomCode && this.username) {
      this.reconnectAttempts++;
      const delay = Math.pow(2, this.reconnectAttempts) * 1000; // Exponential backoff
      console.log(`Attempting reconnect in ${delay}ms... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      setTimeout(() => {
        if (this.roomCode && this.username) {
          this.connect(this.roomCode, this.username);
        }
      }, delay);
    }
  }

  disconnect() {
    this.roomCode = null;
    this.username = null;
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }

  send(type: string, payload: any = {}) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ type, ...payload }));
    } else {
      console.warn('Cannot send message: Socket not open');
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
        gameStore.setRoundEnd(data.round_num, data.scores, data.total_scores, data.game_over, data.winner);
        break;
      
      case 'server_game_over':
        gameStore.setRoundEnd(0, {}, data.final_scores, true, data.winner);
        break;
      
      case 'server_player_left':
        roomStore.updatePlayers(data.players);
        if (data.new_host) roomStore.setHost(data.new_host);
        break;
      
      case 'server_error':
        alert(data.message); // Direct user feedback
        break;
    }
  }
}

export const socketClient = new SocketClient();
