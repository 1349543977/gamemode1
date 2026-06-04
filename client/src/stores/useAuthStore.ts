import { create } from 'zustand';
import type { User } from '../types/user';
import { storage } from '../utils/storage';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setAuth: (user: User, token: string, refreshToken: string) => Promise<void>;
  logout: () => Promise<void>;
  loadFromStorage: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,

  setAuth: async (user, token, refreshToken) => {
    await storage.set('access_token', token);
    await storage.set('refresh_token', refreshToken);
    set({ user, token, isAuthenticated: true });
  },

  logout: async () => {
    await storage.remove('access_token');
    await storage.remove('refresh_token');
    set({ user: null, token: null, isAuthenticated: false });
  },

  loadFromStorage: async () => {
    const token = await storage.get('access_token');
    if (token) { set({ token, isAuthenticated: true }); }
  },
}));
