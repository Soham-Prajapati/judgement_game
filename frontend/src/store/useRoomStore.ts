import { create } from 'zustand';

interface RoomState {
  roomCode: string | null;
  players: string[];
  host: string | null;
  setRoom: (code: string, players: string[], host: string) => void;
  updatePlayers: (players: string[]) => void;
  setHost: (host: string) => void;
  clearRoom: () => void;
}

export const useRoomStore = create<RoomState>((set) => ({
  roomCode: null,
  players: [],
  host: null,
  setRoom: (code, players, host) => set({ roomCode: code, players, host }),
  updatePlayers: (players) => set({ players }),
  setHost: (host) => set({ host }),
  clearRoom: () => set({ roomCode: null, players: [], host: null }),
}));
