import React from 'react';

/**
 * 个人中心页面组件
 * 展示用户信息、观看历史、设置等
 */
export const Profile = () => {
  return (
    <div className="p-4 flex flex-col items-center justify-center h-screen animate-fade-in pb-20">
      <div className="w-20 h-20 rounded-full bg-dark-card mb-4"></div>
      <h1 className="text-xl font-bold mb-2">未登录用户</h1>
      <p className="text-dark-muted mb-8 text-sm">点击登录享受更多权益</p>

      <div className="w-full space-y-2">
        {['观看历史', '我的收藏', '系统设置'].map((item) => (
          <div key={item} className="p-4 bg-dark-card rounded-lg flex justify-between items-center text-sm">
            <span>{item}</span>
            <span className="text-dark-muted">&gt;</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Profile;
