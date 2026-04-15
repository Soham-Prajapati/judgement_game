import React, { useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import { Colors, Typography } from '../core/theme';
import { useGameStore } from '../store/useGameStore';
import { useUserStore } from '../store/useUserStore';
import { useRoomStore } from '../store/useRoomStore';
import { socketClient } from '../services/socketClient';
import CardView from '../components/CardView';
import TrumpIndicator from '../components/TrumpIndicator';
import OpponentStrip from '../components/OpponentStrip';

const GameScreen = ({ navigation }: any) => {
  const { 
    status, roundNum, trumpSuit, hand, bids, tricksWon,
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
      <OpponentStrip 
        players={players}
        currentPlayer={status === 'playing' ? currentPlayer : currentBidder}
        bids={bids}
        tricksWon={tricksWon}
        myUsername={username}
      />

      <View style={styles.subHeader}>
        <Text style={styles.roundText}>ROUND {roundNum}</Text>
        <TrumpIndicator suit={trumpSuit} />
      </View>

      {/* Middle - Trick Area */}
      <View style={styles.playArea}>
        {status === 'bidding' && !isMyTurnToBid && (
          <Text style={styles.waitingText}>Waiting for {currentBidder} to bid...</Text>
        )}
        
        <View style={styles.trickPile}>
          {trickSoFar.map((card, idx) => (
            <CardView key={idx} card={card} size="medium" style={styles.playedCard} />
          ))}
        </View>
        
        {lastTrickResult && trickSoFar.length === 0 && (
          <Text style={styles.winnerText}>{lastTrickResult.winner} won the last trick</Text>
        )}
      </View>

      {/* Bidding Overlay */}
      {isMyTurnToBid && (
        <View style={styles.biddingOverlay}>
          <Text style={styles.biddingTitle}>YOUR BID</Text>
          <Text style={styles.biddingSub}>Choose how many tricks you'll win</Text>
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
                  <Text style={[styles.bidBtnText, isIllegal && { textDecorationLine: 'line-through', color: Colors.neutralMiss }]}>
                    {num}
                  </Text>
                </TouchableOpacity>
              );
            })}
          </ScrollView>
        </View>
      )}

      {/* Bottom - Player Hand */}
      <View style={styles.handArea}>
        <Text style={styles.handTitle}>YOUR HAND</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.handScroll}>
          {hand.map((card, idx) => (
            <CardView 
              key={idx} 
              card={card} 
              size="large"
              style={[styles.cardInHand, !isMyTurnToPlay && { opacity: 0.6 }]}
              onPress={() => isMyTurnToPlay && handlePlayCard(card)}
              disabled={!isMyTurnToPlay}
            />
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
  subHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 10,
  },
  roundText: {
    ...Typography.h2,
    color: Colors.haldiYellow,
  },
  playArea: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  waitingText: {
    ...Typography.body,
    fontStyle: 'italic',
    color: Colors.mutedText,
  },
  trickPile: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    padding: 20,
  },
  playedCard: {
    margin: 5,
    transform: [{ rotate: '5deg' }],
  },
  winnerText: {
    ...Typography.body,
    color: Colors.haldiYellow,
    backgroundColor: 'rgba(0,0,0,0.5)',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 10,
  },
  biddingOverlay: {
    position: 'absolute',
    top: '30%',
    left: '5%',
    width: '90%',
    backgroundColor: Colors.woodDark,
    padding: 24,
    borderRadius: 20,
    alignItems: 'center',
    zIndex: 100,
    borderWidth: 2,
    borderColor: Colors.haldiYellow,
    elevation: 20,
  },
  biddingTitle: {
    ...Typography.h1,
    color: Colors.haldiYellow,
  },
  biddingSub: {
    ...Typography.body,
    color: Colors.mutedText,
    marginBottom: 20,
  },
  bidList: {
    flexDirection: 'row',
  },
  bidBtn: {
    width: 56,
    height: 56,
    backgroundColor: Colors.earthBrown,
    borderRadius: 28,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
    borderWidth: 1,
    borderColor: Colors.woodMid,
  },
  illegalBidBtn: {
    backgroundColor: '#333',
    borderColor: Colors.sindoorRed,
  },
  bidBtnText: {
    ...Typography.h2,
    color: Colors.warmCream,
  },
  handArea: {
    backgroundColor: 'rgba(26, 15, 10, 0.8)',
    paddingTop: 15,
    paddingBottom: 30,
    borderTopLeftRadius: 30,
    borderTopRightRadius: 30,
  },
  handTitle: {
    ...Typography.label,
    color: Colors.mutedText,
    textAlign: 'center',
    marginBottom: 15,
  },
  handScroll: {
    paddingHorizontal: 20,
  },
  cardInHand: {
    marginRight: -30, // Fan effect
  },
});

export default GameScreen;
