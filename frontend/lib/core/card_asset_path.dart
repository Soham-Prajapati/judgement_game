enum Suit {
  spades,
  diamonds,
  hearts,
  clubs,
}

String cardFaceAsset(Suit suit, int rank) {
  if (rank < 1 || rank > 13) {
    throw ArgumentError.value(rank, 'rank', 'rank must be between 1 and 13');
  }
  return 'assets/cards/sprites/${_suitLabel(suit)} $rank.png';
}

String cardBackAsset(int variant) {
  if (variant < 1 || variant > 3) {
    throw ArgumentError.value(variant, 'variant', 'variant must be between 1 and 3');
  }
  return 'assets/cards/sprites/Card Back $variant.png';
}

String emptyCardAsset(int rank) {
  if (rank < 1 || rank > 13) {
    throw ArgumentError.value(rank, 'rank', 'rank must be between 1 and 13');
  }
  return 'assets/cards/sprites/Empty $rank.png';
}

String _suitLabel(Suit suit) {
  switch (suit) {
    case Suit.spades:
      return 'Spades';
    case Suit.diamonds:
      return 'Diamonds';
    case Suit.hearts:
      return 'Hearts';
    case Suit.clubs:
      return 'Clubs';
  }
}