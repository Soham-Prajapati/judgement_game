import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { Colors } from '../core/theme';

interface OpponentStripProps {
  players: string[];
  currentPlayer: string | null;
  bids: Record<string, number>;
  tricksWon: Record<string, number>;
  myUsername: string;
}

const OpponentStrip: React.FC<OpponentStripProps> = ({ 
  players, currentPlayer, bids, tricksWon, myUsername 
}) => {
  return (
    <View style={styles.container}>
      <ScrollView horizontal showsHorizontalScrollIndicator={false}>
        {players.map((player) => {
          const isMe = player === myUsername;
          const isTurn = player === currentPlayer;
          const bid = bids[player];
          const won = tricksWon[player] || 0;

          return (
            <View key={player} style={[styles.avatarCard, isTurn && styles.activeCard]}>
              <Text style={styles.playerName} numberOfLines={1}>
                {isMe ? 'YOU' : player}
              </Text>
              <View style={[styles.bidBadge, isMe && { backgroundColor: Colors.warmCream }]}>
                <Text style={[styles.bidText, isMe && { color: Colors.inkBlack }]}>
                  {bid !== undefined ? `Bid: ${bid}` : '...'}
                </Text>
              </View>
              <Text style={styles.tricksText}>
                Won: {won}
              </Text>
              {isTurn && <View style={styles.turnIndicator} />}
            </View>
          );
        })}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    height: 100,
    backgroundColor: 'rgba(26, 15, 10, 0.6)',
    paddingVertical: 10,
  },
  avatarCard: {
    width: 80,
    height: 80,
    backgroundColor: Colors.woodDark,
    borderRadius: 12,
    marginHorizontal: 8,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: Colors.woodMid,
  },
  activeCard: {
    borderColor: Colors.haldiYellow,
    borderWidth: 2,
    elevation: 10,
  },
  playerName: {
    fontSize: 10,
    fontWeight: 'bold',
    color: Colors.warmCream,
    marginBottom: 4,
  },
  bidBadge: {
    backgroundColor: Colors.haldiYellow,
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
    marginBottom: 4,
  },
  bidText: {
    fontSize: 10,
    fontWeight: 'bold',
    color: Colors.inkBlack,
  },
  tricksText: {
    fontSize: 10,
    color: Colors.mutedText,
  },
  turnIndicator: {
    position: 'absolute',
    bottom: -4,
    width: 20,
    height: 4,
    backgroundColor: Colors.haldiYellow,
    borderRadius: 2,
  },
});

export default OpponentStrip;
