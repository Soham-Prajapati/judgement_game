export const Colors = {
  feltGreen: '#2D5016',
  feltMid: '#3A6B1E',
  earthBrown: '#5C3A1E',
  warmCream: '#F5E6C8',
  haldiYellow: '#E8A020',
  sindoorRed: '#C0392B',
  inkBlack: '#1A0F0A',
  woodDark: '#3D2010',
  woodMid: '#6B4226',
  mutedText: '#B8966A',
  successGreen: '#4CAF50',
  neutralMiss: '#78716C',
  overlayDark: 'rgba(26, 15, 10, 0.85)',
};

export const Typography = {
  display: {
    fontSize: 32,
    color: Colors.warmCream,
    // Note: Fonts will need to be linked separately
    fontFamily: 'TiroDevanagariLatin-Regular', 
  },
  h1: {
    fontSize: 28,
    fontWeight: '700' as const,
    color: Colors.warmCream,
    fontFamily: 'PlayfairDisplay-Bold',
  },
  h2: {
    fontSize: 22,
    fontWeight: '700' as const,
    color: Colors.warmCream,
    fontFamily: 'PlayfairDisplay-Bold',
  },
  h3: {
    fontSize: 18,
    fontWeight: '600' as const,
    color: Colors.warmCream,
    fontFamily: 'DMSans-Medium',
  },
  body: {
    fontSize: 15,
    color: Colors.warmCream,
    fontFamily: 'DMSans-Regular',
  },
  label: {
    fontSize: 13,
    fontWeight: '500' as const,
    color: Colors.inkBlack,
    fontFamily: 'DMSans-Medium',
    textTransform: 'uppercase' as const,
    letterSpacing: 1.5,
  },
  code: {
    fontSize: 24,
    fontWeight: '600' as const,
    color: Colors.haldiYellow,
    fontFamily: 'JetBrainsMono-Bold',
    letterSpacing: 4,
  },
};
