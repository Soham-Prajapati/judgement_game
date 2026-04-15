import axios from 'axios';
import { AppConstants } from '../core/constants';

const api = axios.create({
  baseURL: AppConstants.apiBaseUrl,
  timeout: 5000,
});

export const apiClient = {
  createRoom: async (username: string) => {
    const response = await api.post('/room/create', { username });
    return response.data;
  },
  checkRoomExists: async (code: string) => {
    const response = await api.get(`/room/${code}/exists`);
    return response.data;
  },
};
