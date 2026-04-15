import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Colors, Typography } from '../core/theme';
import { SuitNames } from '../models/card';

interface TrumpIndicatorProps {
  suit: string | null;
}

const TrumpIndicator: React.FC<TrumpIndicatorProps> = ({ suit }) => {
  if (!suit) return null;

  return (
    <View style={styles.container}>
      <Text style={styles.label}>TRUMP</Text>
      <Text style={[styles.suit, (suit === 'H' || suit === 'D') && { color: Colors.sindoorRed }]}>
        {suit}
      </Text>
      <Text style={styles.name}>{SuitNames[suit as keyof typeof SuitNames]}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: Colors.woodDark,
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: Colors.woodMid,
  },
  label: {
    ...Typography.label,
    fontSize: 10,
    color: Colors.mutedText,
    marginRight: 8,
  },
  suit: {
    fontSize: 18,
    fontWeight: 'bold',
    color: Colors.inkBlack,
    marginRight: 4,
  },
  name: {
    ...Typography.body,
    fontSize: 12,
    fontWeight: '600',
    color: Colors.haldiYellow,
  },
});

export default TrumpIndicator;
