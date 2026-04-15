import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import { Colors, Typography } from '../core/theme';
import { useGameStore } from '../store/useGameStore';
import { useUserStore } from '../store/useUserStore';
import { useRoomStore } from '../store/useRoomStore';
import { socketClient } from '../services/socketClient';

const ScoreboardScreen = ({ navigation }: any) => {
  const { status, roundNum, roundScores, totalScores, winner } = useGameStore();
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
      <Text style={Typography.h1}>{status === 'game_over' ? 'Game Over!' : `Round ${roundNum} Ended`}</Text>
      
      {winner && (
        <View style={styles.winnerSection}>
          <Text style={styles.winnerLabel}>WINNER</Text>
          <Text style={styles.winnerName}>{winner}</Text>
        </View>
      )}

      <View style={styles.scoreCard}>
        <View style={styles.scoreRow}>
          <Text style={styles.headerCell}>Player</Text>
          <Text style={styles.headerCell}>Round</Text>
          <Text style={styles.headerCell}>Total</Text>
        </View>
        <ScrollView>
          {players.map((p) => (
            <View key={p} style={styles.scoreRow}>
              <Text style={[styles.cell, p === username && { color: Colors.haldiYellow }]}>{p}</Text>
              <Text style={styles.cell}>+{roundScores[p] || 0}</Text>
              <Text style={styles.cell}>{totalScores[p] || 0}</Text>
            </View>
          ))}
        </ScrollView>
      </View>

      <View style={styles.footer}>
        {username === host ? (
          <TouchableOpacity style={styles.primaryButton} onPress={handleNextAction}>
            <Text style={Typography.label}>
              {status === 'game_over' ? 'Rematch' : 'Next Round'}
            </Text>
          </TouchableOpacity>
        ) : (
          <Text style={styles.waitingText}>Waiting for host...</Text>
        )}
        
        <TouchableOpacity style={styles.exitButton} onPress={handleExit}>
          <Text style={[Typography.label, { color: Colors.sindoorRed }]}>Exit to Home</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.earthBrown,
    padding: 30,
    paddingTop: 60,
  },
  winnerSection: {
    backgroundColor: Colors.woodDark,
    padding: 20,
    borderRadius: 12,
    marginTop: 20,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: Colors.haldiYellow,
  },
  winnerLabel: {
    ...Typography.label,
    color: Colors.mutedText,
  },
  winnerName: {
    ...Typography.display,
    color: Colors.haldiYellow,
  },
  scoreCard: {
    backgroundColor: Colors.woodDark,
    borderRadius: 12,
    marginTop: 30,
    flex: 1,
    padding: 10,
  },
  scoreRow: {
    flexDirection: 'row',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: Colors.woodMid,
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
  },
  footer: {
    marginTop: 20,
  },
  primaryButton: {
    backgroundColor: Colors.haldiYellow,
    padding: 18,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 12,
  },
  exitButton: {
    padding: 18,
    alignItems: 'center',
  },
  waitingText: {
    ...Typography.body,
    color: Colors.mutedText,
    textAlign: 'center',
    fontStyle: 'italic',
    marginBottom: 20,
  },
});

export default ScoreboardScreen;
