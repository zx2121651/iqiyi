import { create } from 'zustand';

interface User {
  id: string;
  name: string;
  isVip: boolean;
  avatar: string;
}

interface AuthState {
  isLogin: boolean;
  user: User | null;
  login: (user: User) => void;
  logout: () => void;
}

const useAuthStore = create<AuthState>((set) => ({
  isLogin: false,
  user: null,
  login: (user) => set({ isLogin: true, user }),
  logout: () => set({ isLogin: false, user: null }),
}));

export default useAuthStore;
