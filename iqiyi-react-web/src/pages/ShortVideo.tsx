import { useEffect, useState, useRef } from 'react';
import request from '@/utils/request';
import { Heart, MessageCircle, Share2, Plus, Link as LinkIcon, Download, MoreHorizontal, X } from 'lucide-react';

interface ShortVideoData {
  id: string;
  authorName: string;
  authorAvatar: string;
  desc: string;
  coverUrl: string;
  likeCount: number;
  commentCount: number;
  shareCount: number;
  isLiked: boolean;
}

/**
 * 随刻 (短视频) 页面组件
 * 使用 CSS Scroll Snap 实现全屏上下滑动切换短视频
 */
export const ShortVideo = () => {
  // 定义状态：短视频列表、加载状态、当前正在播放的视频索引
  const [videos, setVideos] = useState<ShortVideoData[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeIndex, setActiveIndex] = useState(0);
  // 滚动容器的引用，用于计算当前可见的视频
  const containerRef = useRef<HTMLDivElement>(null);
  // 控制分享面板显示隐藏的状态
  const [showSharePanel, setShowSharePanel] = useState(false);

  /**
   * 初始化加载短视频列表数据
   */
  useEffect(() => {
    const fetchVideos = async () => {
      try {
        setLoading(true);
        const res = await request.get<any, ShortVideoData[]>('/short-video/list');
        setVideos(res);
      } catch (error) {
        console.error('获取短视频列表失败:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchVideos();
  }, []);

  /**
   * 格式化数量显示（过万转换）
   */
  const formatCount = (count: number) => {
    if (count > 10000) return (count / 10000).toFixed(1) + 'w';
    return count.toString();
  };

  /**
   * 处理点赞逻辑
   * 找到对应 id 的视频，切换 isLiked 状态并增减点赞数
   */
  const handleLike = (id: string) => {
    setVideos(videos.map(v =>
      v.id === id
        ? { ...v, isLiked: !v.isLiked, likeCount: v.isLiked ? v.likeCount - 1 : v.likeCount + 1 }
        : v
    ));
  };

  /**
   * 监听容器的滚动事件
   * 通过计算 scrollTop 和视口高度 clientHeight 的比值，
   * 得出当前吸附显示在视口中央的视频索引，并更新 activeIndex 触发播放/暂停
   */
  const handleScroll = () => {
    if (!containerRef.current) return;
    const { scrollTop, clientHeight } = containerRef.current;
    // 四舍五入计算当前索引
    const index = Math.round(scrollTop / clientHeight);
    if (index !== activeIndex) {
      setActiveIndex(index);
    }
  };

  if (loading) {
    return <div className="flex h-screen w-full items-center justify-center bg-black text-white">加载中...</div>;
  }

  return (
    // 使用 h-screen 减去底部导航栏高度 (4rem/64px)，这里使用 calc
    <div
      className="w-full h-[calc(100vh-4rem)] bg-black snap-y snap-mandatory overflow-y-scroll no-scrollbar relative"
      ref={containerRef}
      onScroll={handleScroll}
    >
      {/* 顶部透明导航 */}
      <div className="fixed top-0 left-0 right-0 z-10 flex justify-center pt-10 pb-4 bg-gradient-to-b from-black/50 to-transparent pointer-events-none">
        <div className="flex gap-6 text-lg font-bold">
          <span className="text-white/70">关注</span>
          <span className="text-white border-b-2 border-white pb-1">推荐</span>
        </div>
      </div>

      {videos.map((item, index) => (
        <div key={item.id} className="w-full h-full snap-start relative flex items-center justify-center bg-gray-900">
          <video
            src="https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4"
            poster={item.coverUrl}
            className="w-full h-full object-cover opacity-90"
            loop
            muted
            playsInline
            autoPlay={index === activeIndex}
            ref={(el) => {
              if (el) {
                if (index === activeIndex) {
                  el.play().catch(() => {});
                } else {
                  el.pause();
                  el.currentTime = 0;
                }
              }
            }}
          />

          {/* 右侧互动区 */}
          <div className="absolute right-4 bottom-20 flex flex-col items-center gap-6 z-10">
            {/* 头像关注 */}
            <div className="relative">
              <img src={item.authorAvatar} alt="avatar" className="w-12 h-12 rounded-full border-2 border-white" />
              <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 bg-brand rounded-full w-5 h-5 flex items-center justify-center cursor-pointer">
                <Plus size={14} color="white" />
              </div>
            </div>

            {/* 点赞 */}
            <div className="flex flex-col items-center gap-1 cursor-pointer" onClick={() => handleLike(item.id)}>
              <Heart size={32} fill={item.isLiked ? '#ff2b55' : 'transparent'} color={item.isLiked ? '#ff2b55' : 'white'} className={`transition-transform ${item.isLiked ? 'scale-110' : ''}`} />
              <span className="text-white text-xs font-semibold drop-shadow-md">{formatCount(item.likeCount)}</span>
            </div>

            {/* 评论 */}
            <div className="flex flex-col items-center gap-1">
              <MessageCircle size={32} color="white" className="drop-shadow-md" />
              <span className="text-white text-xs font-semibold drop-shadow-md">{formatCount(item.commentCount)}</span>
            </div>

            {/* 分享 */}
            <div className="flex flex-col items-center gap-1 cursor-pointer" onClick={() => setShowSharePanel(true)}>
              <Share2 size={32} color="white" className="drop-shadow-md active:scale-90 transition-transform" />
              <span className="text-white text-xs font-semibold drop-shadow-md">{formatCount(item.shareCount)}</span>
            </div>
          </div>

          {/* 底部信息区 */}
          <div className="absolute left-4 right-20 bottom-4 flex flex-col gap-2 z-10 pointer-events-none">
            <h3 className="text-white text-lg font-bold drop-shadow-md">@{item.authorName}</h3>
            <p className="text-white text-sm line-clamp-2 drop-shadow-md leading-relaxed">{item.desc}</p>
            {/* 音乐滚动条 (模拟) */}
            <div className="flex items-center gap-2 mt-2">
              <span className="text-xs text-white/90 drop-shadow-md bg-white/20 px-2 py-1 rounded-full flex items-center gap-1">
                <span className="animate-spin duration-[3000ms]">🎵</span>
                {item.authorName} 的原声
              </span>
            </div>
          </div>
        </div>
      ))}

      {/* 底部弹出分享面板 */}
      {showSharePanel && (
        <div className="fixed inset-0 z-50 flex flex-col justify-end">
          {/* 半透明遮罩层 */}
          <div
            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
            onClick={() => setShowSharePanel(false)}
          ></div>

          {/* 面板内容 */}
          <div className="relative bg-[#1f1f1f] rounded-t-2xl px-4 pt-6 pb-8 animate-slide-up shadow-[0_-10px_40px_rgba(0,0,0,0.5)]">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-white font-bold">分享到</h3>
              <button onClick={() => setShowSharePanel(false)} className="text-gray-400 p-1">
                <X size={20} />
              </button>
            </div>

            <div className="flex justify-around mb-6">
              <div className="flex flex-col items-center gap-2 cursor-pointer active:scale-95" onClick={() => alert('模拟分享至微信好友')}>
                <div className="w-12 h-12 rounded-full bg-[#09B83E] flex items-center justify-center shadow-lg shadow-[#09B83E]/20">
                  <MessageCircle size={24} color="white" />
                </div>
                <span className="text-xs text-gray-300">微信好友</span>
              </div>
              <div className="flex flex-col items-center gap-2 cursor-pointer active:scale-95" onClick={() => alert('模拟分享至朋友圈')}>
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-[#09B83E] to-[#068A2E] flex items-center justify-center shadow-lg shadow-[#09B83E]/20">
                  <div className="w-6 h-6 border-2 border-white rounded-full flex items-center justify-center">
                    <div className="w-2 h-2 bg-white rounded-full"></div>
                  </div>
                </div>
                <span className="text-xs text-gray-300">朋友圈</span>
              </div>
              <div className="flex flex-col items-center gap-2 cursor-pointer active:scale-95" onClick={() => { alert('链接已复制'); setShowSharePanel(false); }}>
                <div className="w-12 h-12 rounded-full bg-gray-700 flex items-center justify-center">
                  <LinkIcon size={20} color="white" />
                </div>
                <span className="text-xs text-gray-300">复制链接</span>
              </div>
            </div>

            <div className="flex gap-6 border-t border-gray-800 pt-6 overflow-x-auto no-scrollbar pb-2">
               <div className="flex flex-col items-center gap-2 shrink-0 cursor-pointer">
                  <div className="w-10 h-10 rounded-full bg-black/40 border border-gray-700 flex items-center justify-center">
                    <Download size={18} className="text-gray-300" />
                  </div>
                  <span className="text-[10px] text-gray-400">保存本地</span>
               </div>
               <div className="flex flex-col items-center gap-2 shrink-0 cursor-pointer">
                  <div className="w-10 h-10 rounded-full bg-black/40 border border-gray-700 flex items-center justify-center">
                    <MoreHorizontal size={18} className="text-gray-300" />
                  </div>
                  <span className="text-[10px] text-gray-400">更多</span>
               </div>
            </div>

            <button
              className="w-full mt-6 py-3 rounded-full bg-gray-800 text-white font-medium"
              onClick={() => setShowSharePanel(false)}
            >
              取消
            </button>
          </div>
          <style>{`
            @keyframes slideUp {
              from { transform: translateY(100%); }
              to { transform: translateY(0); }
            }
            .animate-slide-up {
              animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            }
          `}</style>
        </div>
      )}
    </div>
  );
};

export default ShortVideo;
