import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import { Colors, Typography } from '../core/theme';
import { useGameStore } from '../store/useGameStore';
import { useUserStore } from '../store/useUserStore';
import { useRoomStore } from '../store/useRoomStore';
import { socketClient } from '../services/socketClient';

const ScoreboardScreen = ({ navigation }: any) => {
  const { status, roundNum, roundScores, totalScores, winner, trumpSuit } = useGameStore();
  const { username } = useUserStore();
  const { host, players } = useRoomStore();

  const handleNextAction = () => {
    if (status === 'game_over') {
      socketClient.send('client_rematch');
    } else {
      socketClient.send('client_next_round');
    }
    navigation.navigate('Game');
  };

  const handleExit = () => {
    socketClient.disconnect();
    useGameStore.getState().resetGame();
    useRoomStore.getState().clearRoom();
    navigation.popToTop();
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{status === 'game_over' ? 'GAME OVER' : `ROUND ${roundNum} SCORES`}</Text>
      
      {winner && status === 'game_over' && (
        <View style={styles.winnerSection}>
          <Text style={styles.winnerLabel}>CHAMPION</Text>
          <Text style={styles.winnerName}>{winner}</Text>
        </View>
      )}

      {!winner && (
        <View style={styles.trumpSummary}>
          <Text style={styles.trumpLabel}>Played with Trump:</Text>
          <Text style={styles.trumpSuit}>{trumpSuit}</Text>
        </View>
      )}

      <View style={styles.scoreCard}>
        <View style={styles.scoreRow}>
          <Text style={[styles.headerCell, { flex: 2, textAlign: 'left' }]}>PLAYER</Text>
          <Text style={styles.headerCell}>ROUND</Text>
          <Text style={styles.headerCell}>TOTAL</Text>
        </View>
        <ScrollView style={styles.scroll}>
          {players.map((p) => (
            <View key={p} style={[styles.scoreRow, p === username && styles.myRow]}>
              <Text style={[styles.cell, { flex: 2, textAlign: 'left', fontWeight: 'bold' }]}>
                {p === username ? 'YOU' : p}
              </Text>
              <Text style={[styles.cell, { color: roundScores[p] > 0 ? Colors.successGreen : Colors.neutralMiss }]}>
                +{roundScores[p] || 0}
              </Text>
              <Text style={[styles.cell, { color: Colors.haldiYellow, fontWeight: 'bold' }]}>
                {totalScores[p] || 0}
              </Text>
            </View>
          ))}
        </ScrollView>
      </View>

      <View style={styles.footer}>
        {username === host ? (
          <TouchableOpacity style={styles.primaryButton} onPress={handleNextAction}>
            <Text style={Typography.label}>
              {status === 'game_over' ? 'PLAY AGAIN' : 'NEXT ROUND'}
            </Text>
          </TouchableOpacity>
        ) : (
          <View style={styles.waitingBadge}>
            <Text style={styles.waitingText}>Waiting for host to continue...</Text>
          </View>
        )}
        
        <TouchableOpacity style={styles.exitButton} onPress={handleExit}>
          <Text style={[Typography.label, { color: Colors.sindoorRed }]}>EXIT TO LOBBY</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.earthBrown,
    padding: 24,
    paddingTop: 60,
  },
  title: {
    ...Typography.h1,
    textAlign: 'center',
    letterSpacing: 2,
  },
  winnerSection: {
    backgroundColor: Colors.woodDark,
    padding: 24,
    borderRadius: 20,
    marginTop: 24,
    alignItems: 'center',
    borderWidth: 3,
    borderColor: Colors.haldiYellow,
    elevation: 10,
  },
  winnerLabel: {
    ...Typography.label,
    color: Colors.mutedText,
    marginBottom: 8,
  },
  winnerName: {
    ...Typography.display,
    color: Colors.haldiYellow,
    fontSize: 40,
  },
  trumpSummary: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 10,
  },
  trumpLabel: {
    ...Typography.body,
    color: Colors.mutedText,
    marginRight: 8,
  },
  trumpSuit: {
    fontSize: 20,
    fontWeight: 'bold',
    color: Colors.haldiYellow,
  },
  scoreCard: {
    backgroundColor: Colors.woodDark,
    borderRadius: 20,
    marginTop: 30,
    flex: 1,
    padding: 16,
    borderWidth: 1,
    borderColor: Colors.woodMid,
  },
  scoreRow: {
    flexDirection: 'row',
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255,255,255,0.05)',
    alignItems: 'center',
  },
  myRow: {
    backgroundColor: 'rgba(232, 160, 32, 0.1)',
    borderRadius: 8,
    paddingHorizontal: 8,
  },
  headerCell: {
    flex: 1,
    ...Typography.label,
    color: Colors.mutedText,
    textAlign: 'center',
  },
  cell: {
    flex: 1,
    ...Typography.body,
    textAlign: 'center',
    fontSize: 16,
  },
  scroll: {
    marginTop: 8,
  },
  footer: {
    marginTop: 24,
    paddingBottom: 20,
  },
  primaryButton: {
    backgroundColor: Colors.haldiYellow,
    padding: 20,
    borderRadius: 16,
    alignItems: 'center',
    marginBottom: 12,
    elevation: 5,
  },
  exitButton: {
    padding: 16,
    alignItems: 'center',
  },
  waitingBadge: {
    backgroundColor: Colors.woodDark,
    padding: 16,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: Colors.woodMid,
    marginBottom: 12,
  },
  waitingText: {
    ...Typography.body,
    color: Colors.mutedText,
    textAlign: 'center',
    fontStyle: 'italic',
  },
});

export default ScoreboardScreen;
