import { useEffect, useState, useRef } from 'react';
import request from '@/utils/request';
import { Heart, MessageCircle, Share2, Plus } from 'lucide-react';

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
  const [videos, setVideos] = useState<ShortVideoData[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeIndex, setActiveIndex] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fetchVideos = async () => {
      try {
        setLoading(true);
        const res = await request.get<any, ShortVideoData[]>('/short-video/list');
        setVideos(res);
      } catch (error) {
        console.error('Failed to load short videos:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchVideos();
  }, []);

  const formatCount = (count: number) => {
    if (count > 10000) return (count / 10000).toFixed(1) + 'w';
    return count.toString();
  };

  const handleLike = (id: string) => {
    setVideos(videos.map(v =>
      v.id === id
        ? { ...v, isLiked: !v.isLiked, likeCount: v.isLiked ? v.likeCount - 1 : v.likeCount + 1 }
        : v
    ));
  };

  const handleScroll = () => {
    if (!containerRef.current) return;
    const { scrollTop, clientHeight } = containerRef.current;
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
            <div className="flex flex-col items-center gap-1">
              <Share2 size={32} color="white" className="drop-shadow-md" />
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
    </div>
  );
};

export default ShortVideo;
