import React from 'react';
import { Settings, Bell, Scan, ChevronRight, PlaySquare, Star, Clock, Download, Wallet, Headphones } from 'lucide-react';

export const Profile = () => {
  const isLogin = false; // 模拟未登录状态

  const services = [
    { icon: <Clock size={28} className="text-orange-400" />, name: '观看历史' },
    { icon: <Star size={28} className="text-yellow-400" />, name: '我的收藏' },
    { icon: <Download size={28} className="text-blue-400" />, name: '离线缓存' },
    { icon: <PlaySquare size={28} className="text-green-400" />, name: '稍后再看' },
  ];

  const tools = [
    { icon: <Wallet size={24} className="text-dark-muted" />, name: '我的钱包', desc: '领红包' },
    { icon: <Headphones size={24} className="text-dark-muted" />, name: '联系客服', desc: '' },
    { icon: <Settings size={24} className="text-dark-muted" />, name: '设置', desc: '' },
  ];

  return (
    <div className="w-full min-h-screen bg-[#121212] text-dark-text pb-20 overflow-y-auto no-scrollbar relative">
      {/* 顶部透明状态栏和操作区 */}
      <div className="flex justify-between items-center px-4 pt-10 pb-4 bg-transparent sticky top-0 z-50">
        <div className="flex gap-4">
          <Scan size={24} />
        </div>
        <div className="flex gap-4">
          <Bell size={24} />
          <Settings size={24} />
        </div>
      </div>

      <div className="px-4">
        {/* 用户头部信息区 */}
        <div className="flex items-center gap-4 mb-6 mt-2">
          <div className="w-16 h-16 rounded-full bg-gray-700 overflow-hidden shadow-lg border-2 border-white/10">
            {/* 头像占位 */}
            <img src="https://dummyimage.com/100x100/333/fff&text=Guest" alt="avatar" className="w-full h-full object-cover" />
          </div>
          <div className="flex flex-col justify-center flex-1">
            <h1 className="text-xl font-bold">{isLogin ? 'VIP用户' : '点击登录/注册'}</h1>
            <p className="text-xs text-dark-muted mt-1">{isLogin ? '爱奇艺号: 12345678' : '登录后享受更多精彩内容'}</p>
          </div>
          <ChevronRight className="text-dark-muted" />
        </div>

        {/* VIP 黑金卡片 */}
        <div className="w-full bg-gradient-to-r from-[#e8c081] to-[#b3853b] rounded-xl p-4 mb-6 shadow-[0_4px_20px_rgba(212,175,55,0.2)] relative overflow-hidden">
          <div className="absolute -right-4 -top-4 w-24 h-24 bg-white/10 rounded-full blur-xl"></div>
          <div className="flex justify-between items-center mb-3">
            <h2 className="text-[#3a280c] text-lg font-black italic">VIP 黄金会员</h2>
            <button className="bg-[#3a280c] text-[#e8c081] text-xs font-bold px-3 py-1.5 rounded-full shadow-md active:scale-95 transition-transform">
              立即开通
            </button>
          </div>
          <p className="text-[#593d14] text-xs font-medium">开通即享万部大片免费看、免广告特权</p>
        </div>

        {/* 核心服务金刚区 (横向滚动) */}
        <div className="bg-[#1f1f1f] rounded-xl p-4 mb-6 shadow-sm">
          <h3 className="text-sm font-bold mb-4 text-white/90">我的服务</h3>
          <div className="flex justify-between">
            {services.map((item, idx) => (
              <div key={idx} className="flex flex-col items-center gap-2 cursor-pointer active:opacity-70 transition-opacity">
                <div className="bg-white/5 p-3 rounded-2xl">
                  {item.icon}
                </div>
                <span className="text-xs text-dark-muted font-medium">{item.name}</span>
              </div>
            ))}
          </div>
        </div>

        {/* 纵向列表菜单区 */}
        <div className="bg-[#1f1f1f] rounded-xl overflow-hidden shadow-sm">
          {tools.map((item, idx) => (
            <div
              key={idx}
              className={`flex items-center justify-between p-4 cursor-pointer active:bg-white/5 transition-colors ${idx !== tools.length - 1 ? 'border-b border-white/5' : ''}`}
            >
              <div className="flex items-center gap-3">
                {item.icon}
                <span className="text-sm font-medium text-white/90">{item.name}</span>
              </div>
              <div className="flex items-center gap-2">
                {item.desc && <span className="text-xs text-dark-muted">{item.desc}</span>}
                <ChevronRight size={18} className="text-dark-muted" />
              </div>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
};

export default Profile;
