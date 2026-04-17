import React, { useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, FlatList, Share } from 'react-native';
import { Colors, Typography } from '../core/theme';
import { useRoomStore } from '../store/useRoomStore';
import { useUserStore } from '../store/useUserStore';
import { useGameStore } from '../store/useGameStore';
import { socketClient } from '../services/socketClient';

const LobbyScreen = ({ navigation }: any) => {
  const { roomCode, players, host } = useRoomStore();
  const { username } = useUserStore();
  const { status } = useGameStore();

  useEffect(() => {
    if (status === 'bidding' || status === 'playing') {
      navigation.navigate('Game');
    }
  }, [navigation, status]);

  const onShare = async () => {
    try {
      await Share.share({
        message: `Join my Judgement game! Room Code: ${roomCode}`,
      });
    } catch (error) {
      console.error(error);
    }
  };

  const handleStart = () => {
    socketClient.send('client_start_game');
  };

  return (
    <View style={styles.container}>
      <Text style={[Typography.body, { color: Colors.mutedText }]}>ROOM CODE</Text>
      <TouchableOpacity onPress={onShare}>
        <Text style={Typography.code}>{roomCode}</Text>
      </TouchableOpacity>

      <Text style={[Typography.h2, { marginTop: 40, marginBottom: 20 }]}>Players ({players.length}/6)</Text>
      
      <FlatList
        data={players}
        keyExtractor={(item) => item}
        renderItem={({ item }) => (
          <View style={styles.playerCard}>
            <View style={styles.playerInfo}>
              <View style={styles.dot} />
              <Text style={styles.playerName}>{item}</Text>
            </View>
            {item === host && (
              <View style={styles.hostBadge}>
                <Text style={styles.hostText}>HOST</Text>
              </View>
            )}
          </View>
        )}
      />

      <View style={styles.footer}>
        {username === host ? (
          <TouchableOpacity 
            style={[styles.startBtn, players.length < 2 && { opacity: 0.5 }]} 
            onPress={handleStart}
            disabled={players.length < 2}
          >
            <Text style={Typography.label}>Start Game</Text>
          </TouchableOpacity>
        ) : (
          <Text style={styles.waitingText}>Waiting for host to start...</Text>
        )}
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
  playerCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: Colors.woodDark,
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: Colors.woodMid,
  },
  playerInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: Colors.successGreen,
    marginRight: 12,
  },
  playerName: {
    ...Typography.body,
    fontSize: 16,
    fontWeight: '500',
  },
  hostBadge: {
    backgroundColor: Colors.haldiYellow,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  hostText: {
    fontSize: 10,
    fontWeight: 'bold',
    color: Colors.inkBlack,
  },
  footer: {
    marginTop: 'auto',
    paddingBottom: 20,
  },
  startBtn: {
    backgroundColor: Colors.haldiYellow,
    padding: 18,
    borderRadius: 12,
    alignItems: 'center',
  },
  waitingText: {
    ...Typography.body,
    color: Colors.mutedText,
    textAlign: 'center',
    fontStyle: 'italic',
  },
});

export default LobbyScreen;
