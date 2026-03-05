import { useEffect, useState } from 'react';
import request from '@/utils/request';
import { useNavigate } from 'react-router-dom';
import { Play } from 'lucide-react';

interface Banner {
  id: string;
  title: string;
  imageUrl: string;
}

interface Video {
  id: string;
  title: string;
  coverUrl: string;
  playCount: number;
  score: number;
  isVip: boolean;
  desc: string;
}

export const Home = () => {
  const navigate = useNavigate();
  const [banners, setBanners] = useState<Banner[]>([]);
  const [videos, setVideos] = useState<Video[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 异步加载首页所需的模拟数据
    const loadHomeData = async () => {
      try {
        setLoading(true);
        const [bannerData, videoData] = await Promise.all([
          request.get<any, Banner[]>('/home/banners'),
          request.get<any, Video[]>('/home/videos'),
        ]);
        setBanners(bannerData);
        setVideos(videoData);
      } catch (error) {
        console.error('Failed to load home data', error);
      } finally {
        setLoading(false);
      }
    };

    loadHomeData();
  }, []);

  // 格式化播放量
  const formatCount = (count: number) => {
    if (count > 10000) return (count / 10000).toFixed(1) + 'w';
    return count.toString();
  };

  return (
    <div className="p-4 flex flex-col gap-4 animate-fade-in pb-20 w-full bg-dark-bg min-h-screen text-dark-text">
      {/* 顶部导航 */}
      <div className="flex justify-between items-center mb-2">
        <h1 className="text-2xl font-bold text-brand tracking-wider italic">iQIYI</h1>
        <div className="flex gap-4 text-sm text-dark-muted">
          <span>推荐</span>
          <span>电视剧</span>
          <span>电影</span>
          <span>综艺</span>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-40">加载中...</div>
      ) : (
        <>
          {/* 轮播图区域 */}
          <div className="w-full h-48 bg-dark-card rounded-lg overflow-hidden relative shadow-lg">
            {banners.length > 0 && (
              <img
                src={banners[0].imageUrl}
                alt={banners[0].title}
                className="w-full h-full object-cover"
              />
            )}
            <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-2">
              <span className="text-white text-sm font-semibold truncate block">
                {banners[0]?.title}
              </span>
            </div>
            {/* 轮播指示器占位 */}
            <div className="absolute bottom-2 right-2 flex gap-1">
              {banners.map((_, idx) => (
                <div
                  key={idx}
                  className={`w-1.5 h-1.5 rounded-full ${idx === 0 ? 'bg-brand w-3' : 'bg-white/50'}`}
                ></div>
              ))}
            </div>
          </div>

          {/* 猜你在追 / 热门推荐 */}
          <div>
            <h2 className="text-lg font-bold mb-3 flex items-center">
              <span>热门推荐</span>
            </h2>
            <div className="grid grid-cols-2 gap-3">
              {videos.map((item) => (
                <div
                  key={item.id}
                  className="flex flex-col gap-1 rounded overflow-hidden"
                  onClick={() => navigate(`/video/${item.id}`)}
                >
                  <div className="relative aspect-[3/4] bg-dark-card rounded-lg overflow-hidden group cursor-pointer">
                    <img src={item.coverUrl} alt={item.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />

                    {/* VIP 标识 */}
                    {item.isVip && (
                      <div className="absolute top-0 right-0 bg-[#D4AF37] text-black text-xs px-1.5 py-0.5 rounded-bl-lg font-bold">
                        VIP
                      </div>
                    )}

                    {/* 评分和播放量 */}
                    <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-1.5 flex justify-between items-end">
                      <span className="text-brand font-bold text-xs">{item.score}</span>
                      <div className="flex items-center text-white/80 text-[10px]">
                        <Play size={10} className="mr-0.5" />
                        {formatCount(item.playCount)}
                      </div>
                    </div>
                  </div>
                  <h3 className="text-sm font-semibold truncate mt-1 text-white">{item.title}</h3>
                  <p className="text-xs text-dark-muted truncate">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Home;
