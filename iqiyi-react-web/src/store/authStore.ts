import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface UserInfo {
  id: string;
  nickname: string;
  avatar: string;
  isVip: boolean;
  vipExpireTime?: string;
}

interface AuthState {
  isLoggedIn: boolean;
  userInfo: UserInfo | null;
  login: (user: UserInfo) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      isLoggedIn: false,
      userInfo: null,
      login: (user) => set({ isLoggedIn: true, userInfo: user }),
      logout: () => set({ isLoggedIn: false, userInfo: null }),
    }),
    {
      name: 'auth-storage', // name of item in the storage (must be unique)
    }
  )
);
