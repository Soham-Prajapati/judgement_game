import { create } from 'zustand';
import { Card } from '../models/card';

interface GameState {
  status: 'lobby' | 'bidding' | 'playing' | 'round_end' | 'game_over';
  roundNum: number;
  trumpSuit: string | null;
  hand: Card[];
  bids: Record<string, number>;
  tricksWon: Record<string, number>;
  currentBidder: string | null;
  illegalBid: number | null;
  currentPlayer: string | null;
  trickSoFar: Card[];
  lastTrickResult: { winner: string; cards: Card[] } | null;
  roundScores: Record<string, number>;
  totalScores: Record<string, number>;
  winner: string | null;

  setStatus: (status: GameState['status']) => void;
  setRoundInfo: (num: number, trump: string) => void;
  setHand: (hand: Card[]) => void;
  setBids: (bids: Record<string, number>) => void;
  setTricksWon: (tricks: Record<string, number>) => void;
  setBidRequest: (bidder: string, illegal: number | null) => void;
  setTurnUpdate: (player: string, trick: Card[]) => void;
  setTrickResult: (winner: string, cards: Card[]) => void;
  setRoundEnd: (num: number, scores: Record<string, number>, totals: Record<string, number>, over: boolean, winner?: string) => void;
  resetGame: () => void;
}

export const useGameStore = create<GameState>((set) => ({
  status: 'lobby',
  roundNum: 0,
  trumpSuit: null,
  hand: [],
  bids: {},
  tricksWon: {},
  currentBidder: null,
  illegalBid: null,
  currentPlayer: null,
  trickSoFar: [],
  lastTrickResult: null,
  roundScores: {},
  totalScores: {},
  winner: null,

  setStatus: (status) => set({ status }),
  setRoundInfo: (num, trump) => set({ roundNum: num, trumpSuit: trump }),
  setHand: (hand) => set({ hand }),
  setBids: (bids) => set({ bids }),
  setTricksWon: (tricks) => set({ tricksWon: tricks }),
  setBidRequest: (bidder, illegal) => set({ currentBidder: bidder, illegalBid: illegal }),
  setTurnUpdate: (player, trick) => set({ currentPlayer: player, trickSoFar: trick, status: 'playing' }),
  setTrickResult: (winner, cards) => set((state) => ({ 
    lastTrickResult: { winner, cards }, 
    trickSoFar: [],
    tricksWon: {
      ...state.tricksWon,
      [winner]: (state.tricksWon[winner] || 0) + 1
    }
  })),
  setRoundEnd: (num, scores, totals, over, winner) => set({
    status: over ? 'game_over' : 'round_end',
    roundNum: num,
    roundScores: scores,
    totalScores: totals,
    winner: winner || null
  }),
  resetGame: () => set({
    status: 'lobby',
    roundNum: 0,
    trumpSuit: null,
    hand: [],
    bids: {},
    tricksWon: {},
    currentBidder: null,
    illegalBid: null,
    currentPlayer: null,
    trickSoFar: [],
    lastTrickResult: null,
    roundScores: {},
    totalScores: {},
    winner: null,
  }),
}));
