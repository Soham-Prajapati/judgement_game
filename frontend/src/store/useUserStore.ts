import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface UserState {
  username: string;
  setUsername: (username: string) => void;
}

export const useUserStore = create<UserState>()(
  persist(
    (set) => ({
      username: '',
      setUsername: (username: string) => set({ username }),
    }),
    {
      name: 'user-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
