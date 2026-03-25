import { useNavigate } from 'react-router-dom';
import { Settings, Clock, Star, Download, Heart, Crown, ChevronRight, History, Bell, MessageSquare } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';

/**
 * 个人中心 (我的) 页面组件
 * 展示用户基本信息、VIP状态，以及各类快捷入口菜单
 */
export const Profile = () => {
  const navigate = useNavigate();
  // 从全局状态获取登录态和用户信息
  const { isLoggedIn, userInfo, logout } = useAuthStore();

  /**
   * 功能入口列表配置
   */
  const menuList = [
    { icon: <Clock size={24} className="text-blue-400" />, label: '历史记录' },
    { icon: <Star size={24} className="text-yellow-400" />, label: '我的收藏' },
    { icon: <Download size={24} className="text-green-400" />, label: '我的下载' },
    { icon: <Heart size={24} className="text-red-400" />, label: '我的点赞' },
  ];

  return (
    <div className="w-full min-h-screen bg-[#121212] text-white pb-20">
      {/* 头部区域：根据登录态展示不同的内容 */}
      <div className="relative pt-12 pb-6 px-6 bg-gradient-to-b from-brand/20 to-transparent">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold italic tracking-wide">我的</h1>
          <button className="p-2" onClick={() => navigate('/settings')}>
            <Settings size={20} className="text-white/80" />
          </button>
        </div>

        {isLoggedIn && userInfo ? (
          // 已登录展示
          <div className="flex items-center gap-4">
            <img src={userInfo.avatar} alt="avatar" className="w-16 h-16 rounded-full border-2 border-brand" />
            <div className="flex flex-col gap-1 flex-1">
              <h2 className="text-xl font-bold">{userInfo.nickname}</h2>
              {userInfo.isVip ? (
                <span className="text-xs bg-[#e8c081] text-[#3a280c] px-2 py-0.5 rounded flex items-center gap-1 self-start font-bold">
                  <Crown size={12} /> VIP会员 (至 {userInfo.vipExpireTime})
                </span>
              ) : (
                <span className="text-xs text-gray-400">普通用户</span>
              )}
            </div>
          </div>
        ) : (
          // 未登录展示
          <div className="flex items-center gap-4 cursor-pointer" onClick={() => navigate('/login')}>
            <div className="w-16 h-16 rounded-full bg-gray-700 flex items-center justify-center border-2 border-gray-600">
              <span className="text-gray-400 text-sm">未登录</span>
            </div>
            <div className="flex flex-col gap-1">
              <h2 className="text-xl font-bold">点击登录/注册</h2>
              <span className="text-xs text-gray-400">登录后畅享高清画质及多端同步记录</span>
            </div>
            <ChevronRight className="ml-auto text-gray-500" />
          </div>
        )}
      </div>

      {/* 快捷金刚区菜单 */}
      <div className="px-4 mb-6">
        <div className="bg-[#1f1f1f] rounded-xl p-4 flex justify-between items-center shadow-lg">
          {menuList.map((item, index) => (
            <div key={index} className="flex flex-col items-center gap-2 cursor-pointer active:scale-95 transition-transform">
              <div className="w-12 h-12 rounded-full bg-black/30 flex items-center justify-center">
                {item.icon}
              </div>
              <span className="text-xs text-gray-300">{item.label}</span>
            </div>
          ))}
        </div>
      </div>

      {/* 其他功能列表 */}
      <div className="px-4">
        <div className="bg-[#1f1f1f] rounded-xl overflow-hidden">
          <div className="px-4 py-4 border-b border-gray-800 flex justify-between items-center cursor-pointer active:bg-white/5">
            <span className="text-sm font-medium">我的预约</span>
            <ChevronRight size={16} className="text-gray-500" />
          </div>
          <div className="px-4 py-4 border-b border-gray-800 flex justify-between items-center cursor-pointer active:bg-white/5">
            <span className="text-sm font-medium">帮助与客服</span>
            <ChevronRight size={16} className="text-gray-500" />
          </div>
          <div className="px-4 py-4 flex justify-between items-center cursor-pointer active:bg-white/5">
            <span className="text-sm font-medium">关于我们</span>
            <ChevronRight size={16} className="text-gray-500" />
          </div>
        </div>

        <div className="bg-[#1a1a1a] rounded-xl overflow-hidden mt-6 mb-8">
          {[
            { icon: <History size={22} className="text-gray-400" />, title: '观看历史' },
            { icon: <Star size={22} className="text-gray-400" />, title: '我的收藏' },
            { icon: <Download size={22} className="text-gray-400" />, title: '离线缓存' },
            { icon: <Bell size={22} className="text-gray-400" />, title: '消息通知' },
            { icon: <MessageSquare size={22} className="text-gray-400" />, title: '帮助与反馈' },
            { icon: <Settings size={22} className="text-gray-400" />, title: '系统设置' },
          ].map((item, index) => (
            <div
              key={item.title}
              className={`flex items-center justify-between p-4 bg-[#222222] active:bg-[#333333] transition-colors cursor-pointer ${
                index !== 5 ? 'border-b border-gray-800' : ''
              }`}
            >
              <div className="flex items-center gap-3">
                {item.icon}
                <span className="text-white text-[15px]">{item.title}</span>
              </div>
              <ChevronRight size={20} className="text-gray-500" />
            </div>
          ))}
        </div>

        {/* 退出登录按钮 */}
        {isLoggedIn && (
          <button
            onClick={() => {
              logout();
            }}
            className="w-full mt-6 py-3 rounded-xl bg-red-500/10 text-red-500 font-bold text-sm active:bg-red-500/20 transition-colors"
          >
            退出登录
          </button>
        )}
      </div>
    </div>
  );
};

export default Profile;
