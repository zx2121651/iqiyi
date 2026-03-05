
import { RouterProvider } from 'react-router-dom';
import router from '@/router';
import { useAppStore } from '@/store/useAppStore';
import { useEffect } from 'react';

function App() {
  const { theme } = useAppStore();

  // 根据状态切换全局主题
  useEffect(() => {
    document.documentElement.className = theme;
  }, [theme]);

  return <RouterProvider router={router} />;
}

export default App;
