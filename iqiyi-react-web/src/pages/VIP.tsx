import { useEffect, useState } from 'react';
import request from '@/utils/request';
import { Crown, ChevronRight } from 'lucide-react';

interface Privilege {
  icon: string;
  name: string;
  desc: string;
}

interface VipVideo {
  id: string;
  title: string;
  coverUrl: string;
  score: number;
  desc: string;
}

/**
 * VIP 会员中心页面组件
 * 展示会员开通信息、专属特权、及 VIP 推荐影视
 */
export const VIP = () => {
  // 定义状态：会员特权列表、VIP推荐影视列表、加载状态
  const [privileges, setPrivileges] = useState<Privilege[]>([]);
  const [recommends, setRecommends] = useState<VipVideo[]>([]);
  const [loading, setLoading] = useState(true);

  /**
   * 并发请求加载 VIP 页面所需的基础数据（特权信息和推荐影视）
   */
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [privData, recData] = await Promise.all([
          request.get<any, Privilege[]>('/vip/privileges'),
          request.get<any, VipVideo[]>('/vip/recommends'),
        ]);
        setPrivileges(privData);
        setRecommends(recData);
      } catch (error) {
        console.error('获取VIP数据失败:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return <div className="flex h-screen w-full items-center justify-center bg-[#121212] text-[#D4AF37]">加载特权中...</div>;
  }

  return (
    <div className="w-full min-h-screen bg-[#121212] text-dark-text pb-20 overflow-y-auto no-scrollbar relative">
      {/* 顶部标题栏 */}
      <div className="flex justify-center items-center px-4 pt-10 pb-4 bg-transparent sticky top-0 z-50">
        <h1 className="text-xl font-bold text-[#e8c081] flex items-center gap-2">
          <Crown size={24} /> 会员中心
        </h1>
      </div>

      <div className="px-4">
        {/* 会员开通卡片 */}
        <div className="w-full bg-gradient-to-br from-[#1f1a14] to-[#3a280c] border border-[#593d14] rounded-2xl p-5 mb-6 relative overflow-hidden shadow-2xl">
          <div className="absolute top-0 right-0 w-32 h-32 bg-[#e8c081]/10 rounded-full blur-2xl"></div>

          <div className="flex justify-between items-start mb-6">
            <div>
              <h2 className="text-[#e8c081] text-2xl font-black italic tracking-wide">VIP 黄金会员</h2>
              <p className="text-[#a3793e] text-xs mt-1">未开通 | 预计为你节省 ¥1200</p>
            </div>
          </div>

          <div className="flex gap-3 mb-6">
            <div className="flex-1 bg-black/30 border border-[#e8c081]/30 rounded-xl p-3 flex flex-col items-center justify-center relative">
              <div className="absolute -top-2 left-1/2 -translate-x-1/2 bg-[#ff3b30] text-white text-[10px] px-2 py-0.5 rounded-full whitespace-nowrap">
                限时特惠
              </div>
              <span className="text-[#a3793e] text-xs line-through mt-1">¥258</span>
              <div className="text-[#e8c081] font-bold mt-1 flex items-baseline gap-1">
                <span className="text-sm">¥</span><span className="text-2xl">148</span><span className="text-xs">/年</span>
              </div>
            </div>
            <div className="flex-1 bg-black/20 border border-[#e8c081]/10 rounded-xl p-3 flex flex-col items-center justify-center opacity-80">
              <span className="text-[#a3793e] text-xs">连续包季</span>
              <div className="text-[#e8c081] font-bold mt-1 flex items-baseline gap-1">
                <span className="text-sm">¥</span><span className="text-xl">45</span><span className="text-xs">/季</span>
              </div>
            </div>
          </div>

          <button className="w-full bg-gradient-to-r from-[#e8c081] to-[#c29653] text-[#3a280c] py-3 rounded-full font-bold text-sm shadow-[0_4px_15px_rgba(212,175,55,0.3)] active:scale-95 transition-transform flex items-center justify-center gap-2">
            确认协议并支付 <ChevronRight size={16} />
          </button>
        </div>

        {/* 专属特权金刚区 */}
        <div className="bg-[#1f1f1f] rounded-xl p-4 mb-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-[#e8c081] text-sm font-bold flex items-center gap-1">
              VIP 专属特权 <span className="text-[#a3793e] text-xs font-normal">共40+项特权</span>
            </h3>
            <span className="text-xs text-dark-muted flex items-center">全部 <ChevronRight size={12} /></span>
          </div>
          <div className="grid grid-cols-3 gap-y-4">
            {privileges.map((item, idx) => (
              <div key={idx} className="flex flex-col items-center gap-1.5 cursor-pointer">
                <div className="w-10 h-10 bg-black/40 rounded-full flex items-center justify-center border border-[#e8c081]/20 text-xl">
                  {item.icon}
                </div>
                <span className="text-[#e8c081] text-xs font-medium">{item.name}</span>
                <span className="text-dark-muted text-[10px]">{item.desc}</span>
              </div>
            ))}
          </div>
        </div>

        {/* VIP 专享影视流 */}
        <div>
          <h3 className="text-[#e8c081] text-lg font-bold mb-3 flex items-center">
            为你推荐 <span className="ml-2 text-xs text-dark-muted font-normal bg-[#3a280c]/50 px-2 py-0.5 rounded text-[#a3793e]">尊贵之选</span>
          </h3>
          <div className="grid grid-cols-2 gap-3">
            {recommends.map((item) => (
              <div key={item.id} className="flex flex-col gap-1 rounded overflow-hidden">
                <div className="relative aspect-[3/4] bg-[#1f1f1f] rounded-lg overflow-hidden group">
                  <img src={item.coverUrl} alt={item.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />

                  {/* VIP 金色标识 */}
                  <div className="absolute top-0 right-0 bg-[#e8c081] text-[#3a280c] text-[10px] px-1.5 py-0.5 rounded-bl-lg font-black tracking-wide">
                    VIP
                  </div>

                  <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/90 to-transparent p-1.5 flex justify-between items-end">
                    <span className="text-[#e8c081] font-bold text-xs">{item.score}</span>
                  </div>
                </div>
                <h3 className="text-sm font-semibold truncate mt-1 text-white">{item.title}</h3>
                <p className="text-xs text-[#a3793e] truncate">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
};

export default VIP;
