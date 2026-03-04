import { create } from 'zustand';

interface AppState {
  theme: 'dark' | 'light';
  setTheme: (theme: 'dark' | 'light') => void;
}

/**
 * 全局状态管理
 * 使用 Zustand 管理简单的全局状态，例如主题等。
 */
export const useAppStore = create<AppState>((set) => ({
  theme: 'dark', // 默认深色模式，符合视频网站风格
  setTheme: (theme) => set({ theme }),
}));
