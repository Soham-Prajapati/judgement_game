export interface Card {
  suit: 'S' | 'D' | 'H' | 'C';
  rank: string;
}

export const SuitNames = {
  S: 'Spades',
  D: 'Diamonds',
  H: 'Hearts',
  C: 'Clubs',
};
