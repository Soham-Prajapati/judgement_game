import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, TextInput, Modal } from 'react-native';
import { Colors, Typography } from '../core/theme';
import { useUserStore } from '../store/useUserStore';
import { apiClient } from '../services/apiClient';
import { socketClient } from '../services/socketClient';
import { useRoomStore } from '../store/useRoomStore';

const HomeScreen = ({ navigation }: any) => {
  const { username, setUsername } = useUserStore();
  const [showUserModal, setShowUserModal] = useState(false);
  const [tempName, setTempName] = useState('');

  useEffect(() => {
    if (!username) {
      setShowUserModal(true);
    }
  }, [username]);

  const handleCreateRoom = async () => {
    if (!username) return setShowUserModal(true);
    try {
      const response = await apiClient.createRoom(username);
      socketClient.connect(response.room_code, username);
      navigation.navigate('Lobby', { roomCode: response.room_code });
    } catch (error) {
      console.error(error);
    }
  };

  const saveUsername = () => {
    if (tempName.trim()) {
      setUsername(tempName.trim());
      setShowUserModal(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={Typography.display}>JUDGEMENT</Text>
      <Text style={styles.subtitle}>Kachuful • 2-6 Players</Text>

      <View style={styles.actions}>
        <Text style={styles.playingAs}>Playing as: {username || 'Guest'}</Text>
        <TouchableOpacity style={styles.primaryButton} onPress={handleCreateRoom}>
          <Text style={Typography.label}>Create Room</Text>
        </TouchableOpacity>
        <TouchableOpacity 
          style={styles.secondaryButton} 
          onPress={() => navigation.navigate('JoinRoom')}
        >
          <Text style={[Typography.label, { color: Colors.warmCream }]}>Join Room</Text>
        </TouchableOpacity>
      </View>

      <Modal visible={showUserModal} transparent animationType="fade">
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={Typography.h2}>Enter Username</Text>
            <TextInput
              style={styles.input}
              placeholder="e.g. CardMaster"
              placeholderTextColor={Colors.mutedText}
              value={tempName}
              onChangeText={setTempName}
              maxLength={16}
            />
            <TouchableOpacity style={styles.primaryButton} onPress={saveUsername}>
              <Text style={Typography.label}>Start Playing</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.earthBrown,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  subtitle: {
    ...Typography.body,
    color: Colors.mutedText,
    marginTop: 8,
  },
  actions: {
    width: '100%',
    marginTop: 60,
  },
  playingAs: {
    ...Typography.body,
    color: Colors.mutedText,
    textAlign: 'center',
    marginBottom: 16,
  },
  primaryButton: {
    backgroundColor: Colors.haldiYellow,
    padding: 18,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 16,
  },
  secondaryButton: {
    borderWidth: 2,
    borderColor: Colors.warmCream,
    padding: 18,
    borderRadius: 12,
    alignItems: 'center',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.8)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: Colors.woodDark,
    padding: 30,
    borderRadius: 20,
    width: '80%',
    borderWidth: 1,
    borderColor: Colors.woodMid,
  },
  input: {
    backgroundColor: Colors.inkBlack,
    color: Colors.warmCream,
    padding: 12,
    borderRadius: 10,
    marginTop: 20,
    marginBottom: 20,
    fontSize: 16,
  },
});

export default HomeScreen;
