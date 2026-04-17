import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, TextInput } from 'react-native';
import { Colors, Typography } from '../core/theme';
import { apiClient } from '../services/apiClient';
import { socketClient } from '../services/socketClient';
import { useUserStore } from '../store/useUserStore';

const JoinRoomScreen = ({ navigation }: any) => {
  const [code, setCode] = useState('');
  const [error, setError] = useState('');
  const { username } = useUserStore();

  const handleJoin = async () => {
    if (code.length < 6) return;
    try {
      const response = await apiClient.checkRoomExists(code.toUpperCase());
      if (response.exists) {
        if (response.player_count >= 6) {
          setError('Room is full');
          return;
        }
        socketClient.connect(code.toUpperCase(), username);
        navigation.navigate('Lobby', { roomCode: code.toUpperCase() });
      } else {
        setError('Room not found');
      }
    } catch {
      setError('Error connecting to server');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={Typography.h1}>Join Room</Text>
      
      <TextInput
        style={styles.input}
        placeholder="ENTER CODE"
        placeholderTextColor={Colors.mutedText}
        value={code}
        onChangeText={(val) => setCode(val.toUpperCase())}
        autoCapitalize="characters"
        maxLength={6}
      />
      
      {error ? <Text style={styles.error}>{error}</Text> : null}

      <TouchableOpacity 
        style={[styles.button, code.length < 6 && { opacity: 0.5 }]} 
        onPress={handleJoin}
        disabled={code.length < 6}
      >
        <Text style={Typography.label}>Join</Text>
      </TouchableOpacity>
      
      <TouchableOpacity onPress={() => navigation.goBack()}>
        <Text style={[Typography.body, { color: Colors.mutedText, marginTop: 20 }]}>Go Back</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.earthBrown,
    padding: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  input: {
    ...Typography.code,
    backgroundColor: Colors.woodDark,
    width: '100%',
    padding: 20,
    borderRadius: 12,
    marginTop: 40,
    marginBottom: 10,
    textAlign: 'center',
    borderWidth: 1,
    borderColor: Colors.woodMid,
  },
  button: {
    backgroundColor: Colors.haldiYellow,
    width: '100%',
    padding: 18,
    borderRadius: 12,
    alignItems: 'center',
    marginTop: 20,
  },
  error: {
    color: Colors.sindoorRed,
    marginTop: 5,
    fontSize: 14,
  },
});

export default JoinRoomScreen;
