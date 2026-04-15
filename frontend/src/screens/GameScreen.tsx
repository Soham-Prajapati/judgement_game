import React, { useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import { Colors, Typography } from '../core/theme';
import { useGameStore } from '../store/useGameStore';
import { useUserStore } from '../store/useUserStore';
import { useRoomStore } from '../store/useRoomStore';
import { socketClient } from '../services/socketClient';
import { SuitNames } from '../models/card';

const GameScreen = ({ navigation }: any) => {
  const { 
    status, roundNum, trumpSuit, hand, bids, 
    currentBidder, illegalBid, currentPlayer, 
    trickSoFar, lastTrickResult 
  } = useGameStore();
  const { username } = useUserStore();
  const { players } = useRoomStore();

  useEffect(() => {
    if (status === 'round_end' || status === 'game_over') {
      navigation.navigate('Scoreboard');
    }
  }, [status]);

  const handlePlaceBid = (bid: number) => {
    socketClient.send('client_place_bid', { bid });
  };

  const handlePlayCard = (card: any) => {
    socketClient.send('client_play_card', { card });
  };

  const isMyTurnToBid = status === 'bidding' && currentBidder === username;
  const isMyTurnToPlay = status === 'playing' && currentPlayer === username;

  return (
    <View style={styles.container}>
      {/* Top Bar - Opponents */}
      <View style={styles.header}>
        <Text style={Typography.h3}>Round {roundNum}</Text>
        <View style={styles.trumpBadge}>
          <Text style={styles.trumpText}>TRUMP: {trumpSuit ? SuitNames[trumpSuit as keyof typeof SuitNames] : '?'}</Text>
        </View>
      </View>

      {/* Middle - Trick Area */}
      <View style={styles.playArea}>
        <Text style={[Typography.body, { color: Colors.mutedText }]}>
          {status === 'playing' ? `${currentPlayer}'s turn` : 'Bidding phase...'}
        </Text>
        <View style={styles.trickPile}>
          {trickSoFar.map((card, idx) => (
            <View key={idx} style={styles.playedCard}>
              <Text style={styles.cardText}>{card.rank}{card.suit}</Text>
            </View>
          ))}
        </View>
        {lastTrickResult && (
          <Text style={styles.winnerText}>{lastTrickResult.winner} won the last trick</Text>
        )}
      </View>

      {/* Bidding Overlay (Functional Placeholder) */}
      {isMyTurnToBid && (
        <View style={styles.biddingOverlay}>
          <Text style={Typography.h2}>Your Bid</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.bidList}>
            {Array.from({ length: (8 - roundNum) + 1 }, (_, i) => i).map((num) => {
              const isIllegal = num === illegalBid;
              return (
                <TouchableOpacity 
                  key={num} 
                  style={[styles.bidBtn, isIllegal && styles.illegalBidBtn]} 
                  onPress={() => !isIllegal && handlePlaceBid(num)}
                  disabled={isIllegal}
                >
                  <Text style={[styles.bidBtnText, isIllegal && { textDecorationLine: 'line-through' }]}>{num}</Text>
                </TouchableOpacity>
              );
            })}
          </ScrollView>
        </View>
      )}

      {/* Bottom - Player Hand */}
      <View style={styles.handArea}>
        <Text style={styles.handTitle}>YOUR HAND ({hand.length})</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.handScroll}>
          {hand.map((card, idx) => (
            <TouchableOpacity 
              key={idx} 
              style={[styles.card, !isMyTurnToPlay && { opacity: 0.6 }]}
              onPress={() => isMyTurnToPlay && handlePlayCard(card)}
              disabled={!isMyTurnToPlay}
            >
              <Text style={[styles.cardRank, (card.suit === 'H' || card.suit === 'D') && { color: Colors.sindoorRed }]}>
                {card.rank}
              </Text>
              <Text style={[styles.cardSuit, (card.suit === 'H' || card.suit === 'D') && { color: Colors.sindoorRed }]}>
                {card.suit}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.feltGreen,
  },
  header: {
    paddingTop: 50,
    paddingHorizontal: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  trumpBadge: {
    backgroundColor: Colors.woodDark,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  trumpText: {
    color: Colors.haldiYellow,
    fontWeight: 'bold',
    fontSize: 12,
  },
  playArea: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  trickPile: {
    flexDirection: 'row',
    marginTop: 20,
    minHeight: 100,
  },
  playedCard: {
    width: 60,
    height: 80,
    backgroundColor: Colors.warmCream,
    borderRadius: 8,
    margin: 5,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 5,
  },
  cardText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: Colors.inkBlack,
  },
  winnerText: {
    ...Typography.body,
    marginTop: 20,
    color: Colors.haldiYellow,
  },
  handArea: {
    backgroundColor: 'rgba(0,0,0,0.4)',
    paddingVertical: 20,
  },
  handTitle: {
    ...Typography.label,
    color: Colors.mutedText,
    textAlign: 'center',
    marginBottom: 10,
  },
  handScroll: {
    paddingHorizontal: 20,
  },
  card: {
    width: 70,
    height: 100,
    backgroundColor: Colors.warmCream,
    borderRadius: 10,
    marginRight: 10,
    padding: 10,
    justifyContent: 'space-between',
  },
  cardRank: {
    fontSize: 20,
    fontWeight: 'bold',
    color: Colors.inkBlack,
  },
  cardSuit: {
    fontSize: 24,
    textAlign: 'right',
    color: Colors.inkBlack,
  },
  biddingOverlay: {
    position: 'absolute',
    top: '30%',
    left: '10%',
    width: '80%',
    backgroundColor: Colors.woodDark,
    padding: 20,
    borderRadius: 20,
    alignItems: 'center',
    zIndex: 10,
    borderWidth: 2,
    borderColor: Colors.haldiYellow,
  },
  bidList: {
    marginTop: 20,
    flexDirection: 'row',
  },
  bidBtn: {
    width: 50,
    height: 50,
    backgroundColor: Colors.earthBrown,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 10,
  },
  illegalBidBtn: {
    opacity: 0.3,
    borderColor: Colors.sindoorRed,
    borderWidth: 1,
  },
  bidBtnText: {
    color: Colors.warmCream,
    fontSize: 18,
    fontWeight: 'bold',
  },
});

export default GameScreen;
