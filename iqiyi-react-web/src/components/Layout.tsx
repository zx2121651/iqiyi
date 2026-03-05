
import { NavLink, Outlet } from 'react-router-dom';
import { Home, PlaySquare, Crown, User } from 'lucide-react';
import classNames from 'classnames';

/**
 * 底部导航栏组件 (Layout)
 * 包装整个应用的主体，固定在底部的导航菜单
 */
export const Layout = () => {
  const tabs = [
    { name: '首页', path: '/', icon: <Home size={24} /> },
    { name: '随刻', path: '/short-video', icon: <PlaySquare size={24} /> },
    { name: '会员', path: '/vip', icon: <Crown size={24} /> },
    { name: '我的', path: '/profile', icon: <User size={24} /> },
  ];

  return (
    <div className="flex flex-col h-screen w-full bg-dark-bg text-dark-text overflow-hidden">
      {/* 页面主内容区，支持滚动 */}
      <div className="flex-1 overflow-y-auto">
        <Outlet />
      </div>

      {/* 固定的底部导航栏 */}
      <div className="fixed bottom-0 left-0 right-0 h-16 bg-dark-card border-t border-gray-800 flex justify-around items-center z-50">
        {tabs.map((tab) => (
          <NavLink
            key={tab.path}
            to={tab.path}
            className={({ isActive }) =>
              classNames(
                'flex flex-col items-center justify-center w-full h-full gap-1 transition-colors duration-200',
                isActive ? 'text-brand font-bold' : 'text-dark-muted hover:text-gray-300'
              )
            }
          >
            {tab.icon}
            <span className="text-xs">{tab.name}</span>
          </NavLink>
        ))}
      </div>
    </div>
  );
};

export default Layout;
