import React from 'react';
import { createBrowserRouter } from 'react-router-dom';
import Layout from '@/components/Layout';
import Home from '@/pages/Home';
import ShortVideo from '@/pages/ShortVideo';
import VIP from '@/pages/VIP';
import Profile from '@/pages/Profile';

/**
 * 路由配置对象
 * 使用 react-router-dom 的 browserRouter 管理页面跳转
 */
export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { path: '/', element: <Home /> },
      { path: '/short-video', element: <ShortVideo /> },
      { path: '/vip', element: <VIP /> },
      { path: '/profile', element: <Profile /> },
    ],
  },
  // 未匹配到的路由可以添加一个 404 页面
  {
    path: '*',
    element: <div className="p-10 text-center text-white">404 - 页面未找到</div>,
  },
]);

export default router;
