import { useEffect, useState } from 'react';
import request from '@/utils/request';
import { useNavigate } from 'react-router-dom';
import { Play, Search, Loader2, Crown, Sparkles, Film, Gamepad2, Music } from 'lucide-react';
import { motion, useAnimation } from 'framer-motion';
import { useRef } from 'react';

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

/**
 * 首页组件
 * 包含：顶部导航、轮播图、金刚区分类、继续观看、重磅热播横向列表、特色排版专区、热门推荐瀑布流
 */
export const Home = () => {
  const navigate = useNavigate();
  // 定义状态：轮播图数据、视频列表数据、加载状态、当前激活的分类Tab、下拉刷新状态、上拉加载状态
  const [banners, setBanners] = useState<Banner[]>([]);
  const [videos, setVideos] = useState<Video[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('推荐');
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [page, setPage] = useState(1);

  // 顶部导航分类列表
  const tabs = ['推荐', '电视剧', '电影', '综艺'];
  // framer-motion 用于控制下拉刷新时的位移动画
  const controls = useAnimation();
  // 容器引用，用于监听滚动事件以实现触底加载
  const containerRef = useRef<HTMLDivElement>(null);

  /**
   * 加载首页数据
   * 并发请求轮播图和视频列表，使用 mock 数据
   */
  const loadHomeData = async () => {
    try {
      setLoading(true);
      const [bannerData, videoData] = await Promise.all([
        request.get<any, Banner[]>('/home/banners'),
        request.get<any, Video[]>('/home/videos'),
      ]);
      // 模拟根据不同的 Tab 切换打乱数据展示顺序
      setBanners(bannerData.sort(() => Math.random() - 0.5));
      setVideos(videoData.sort(() => Math.random() - 0.5));
    } catch (error) {
      console.error('Failed to load home data', error);
    } finally {
      setLoading(false);
    }
  };

  // 当 activeTab 改变时，重新拉取/刷新数据
  useEffect(() => {
    setPage(1); // 切换 Tab 时重置页码
    loadHomeData();
  }, [activeTab]);

  /**
   * 处理手动下拉刷新逻辑
   * 触发 framer-motion 动画展示刷新中，并模拟延迟
   */
  const handleRefresh = async () => {
    setIsRefreshing(true);
    setPage(1); // 刷新重置页码
    // 向下移动 50px 模拟下拉效果
    await controls.start({ y: 50 });
    // 模拟网络延迟 1 秒
    await new Promise(resolve => setTimeout(resolve, 1000));
    // 打乱数据模拟刷新
    setBanners(prev => [...prev].sort(() => Math.random() - 0.5));
    setVideos(prev => [...prev].sort(() => Math.random() - 0.5));
    // 恢复原位
    await controls.start({ y: 0 });
    setIsRefreshing(false);
  };

  /**
   * 监听容器滚动事件
   * 用于实现触底自动加载更多数据
   */
  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    const { scrollTop, scrollHeight, clientHeight } = e.currentTarget;

    // 如果滚动到顶部且没有在刷新，可以扩展为原生的下拉刷新触发（此处为了简化，在界面上提供了点击刷新代替）
    if (scrollTop === 0 && !isRefreshing) {
      // 触顶下拉 (由于我们没有原生的touch事件监听，这里简单用点击顶部区域代替下拉刷新演示，
      // 或者依赖特定的拉拽库。为简化原生模拟，我们在顶部增加一个明显的刷新按钮/提示框区域)
    }

    // 触底加载更多：当距离底部不足 50px 且没有正在加载或刷新时，触发加载更多
    if (scrollHeight - scrollTop <= clientHeight + 50 && !isLoadingMore && !loading) {
      loadMoreData();
    }
  };

  const kingKongList = [
    { name: 'VIP专区', icon: <Crown size={24} className="text-[#e8c081]" />, bg: 'bg-[#3a280c]' },
    { name: '动漫', icon: <Sparkles size={24} className="text-purple-400" />, bg: 'bg-purple-500/20' },
    { name: '纪录片', icon: <Film size={24} className="text-blue-400" />, bg: 'bg-blue-500/20' },
    { name: '游戏', icon: <Gamepad2 size={24} className="text-green-400" />, bg: 'bg-green-500/20' },
    { name: '音乐', icon: <Music size={24} className="text-pink-400" />, bg: 'bg-pink-500/20' },
  ];

  /**
   * 加载更多数据逻辑 (模拟真实分页)
   * 根据当前页码生成不同后缀的标题，模拟加载下一页的数据
   */
  const loadMoreData = async () => {
    setIsLoadingMore(true);
    await new Promise(resolve => setTimeout(resolve, 1000));

    const nextPage = page + 1;
    // 模拟基于原数据生成带有“第 X 页”后缀的新数据
    const moreVideos = videos.slice(0, 4).map(v => ({
      ...v,
      id: v.id + '_page_' + nextPage + '_' + Date.now(),
      title: v.title.replace(/\s*\(新第\d+页\)$/, '') + ` (新第${nextPage}页)`,
      playCount: Math.floor(Math.random() * 50000)
    }));

    setVideos(prev => [...prev, ...moreVideos]);
    setPage(nextPage);
    setIsLoadingMore(false);
  };

  /**
   * 格式化播放量数字
   * @param count 播放量数值
   * @returns 转换后带单位的字符串 (如 1.5w)
   */
  const formatCount = (count: number) => {
    if (count > 10000) return (count / 10000).toFixed(1) + 'w';
    return count.toString();
  };

  return (
    <div
      ref={containerRef}
      onScroll={handleScroll}
      className="p-4 flex flex-col gap-4 animate-fade-in pb-20 w-full bg-dark-bg min-h-screen text-dark-text overflow-y-auto"
    >
      {/* 顶部导航 */}
      <div className="flex justify-between items-center mb-2 sticky top-0 bg-dark-bg z-10 py-2">
        <h1 className="text-2xl font-bold text-brand tracking-wider italic">iQIYI</h1>
        <div className="flex gap-4 text-sm text-dark-muted items-center">
          {tabs.map((tab) => (
            <span
              key={tab}
              className={`cursor-pointer transition-colors ${activeTab === tab ? 'text-white font-bold' : 'hover:text-white/80'}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab}
            </span>
          ))}
          <Search size={18} className="text-white ml-2 cursor-pointer" onClick={() => navigate('/search')} />
        </div>
      </div>

      {loading && videos.length === 0 ? (
        <div className="flex justify-center items-center h-40">加载中...</div>
      ) : (
        <motion.div animate={controls}>
          {isRefreshing && (
            <div className="flex justify-center items-center text-brand text-xs mb-2 gap-1 absolute top-[-30px] left-1/2 -translate-x-1/2">
              <Loader2 size={14} className="animate-spin" /> 正在刷新...
            </div>
          )}

          {/* 手动刷新触发区 (由于没加拖拽库，提供一个点击刷新的替代方案) */}
          <div className="text-center text-[10px] text-dark-muted mb-2 cursor-pointer" onClick={handleRefresh}>
            下拉或点击刷新
          </div>

          {/* 轮播图区域 */}
          <div className="w-full h-48 bg-dark-card rounded-lg overflow-hidden relative shadow-lg mb-4">
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

          {/* 分类金刚区 (Kingkong 图标导航) */}
          <div className="flex justify-between items-center mb-4 px-2">
            {kingKongList.map((item, index) => (
              <motion.div
                key={index}
                className="flex flex-col items-center gap-1.5 cursor-pointer"
                whileTap={{ scale: 0.9 }}
                onClick={() => alert(`点击分类: ${item.name}`)}
              >
                <div className={`w-12 h-12 rounded-full flex items-center justify-center ${item.bg}`}>
                  {item.icon}
                </div>
                <span className="text-xs text-white/80 font-medium">{item.name}</span>
              </motion.div>
            ))}
          </div>

          {/* 继续观看 (新加模块) */}
          <div className="mb-4 bg-[#1f1f1f] rounded-lg p-3 flex items-center justify-between shadow-sm cursor-pointer hover:bg-[#2a2a2a] transition-colors" onClick={() => navigate(`/video/v1`)}>
            <div className="flex flex-col gap-1">
              <span className="text-xs text-dark-muted font-medium">上次观看到 12:45</span>
              <span className="text-sm text-white font-bold truncate max-w-[200px]">三体 第12集</span>
            </div>
            <div className="w-10 h-10 rounded-full bg-brand/20 flex items-center justify-center text-brand">
              <Play size={20} className="ml-1" />
            </div>
          </div>

          {/* 重磅热播 (横向滚动列表) */}
          <div className="mb-6">
            <h2 className="text-lg font-bold mb-3 text-white">重磅热播</h2>
            <div className="flex gap-3 overflow-x-auto no-scrollbar pb-2">
              {videos.slice(0, 5).map((item) => (
                <motion.div
                  key={`hot-${item.id}`}
                  className="w-[120px] flex-shrink-0 flex flex-col gap-1 cursor-pointer"
                  whileTap={{ scale: 0.95 }}
                  onClick={() => navigate(`/video/${item.id}`)}
                >
                  <div className="relative aspect-[3/4] rounded-lg overflow-hidden">
                    <img src={item.coverUrl} className="w-full h-full object-cover" alt={item.title} />
                    {item.isVip && <div className="absolute top-0 right-0 bg-[#D4AF37] text-black text-[10px] px-1 rounded-bl-lg font-bold">VIP</div>}
                  </div>
                  <span className="text-xs font-semibold text-white/90 truncate mt-1">{item.title}</span>
                </motion.div>
              ))}
            </div>
          </div>

          {/* 专属频道卡片 (如“正在热播”、“即将上线”) */}
          <div className="mb-6 p-4 rounded-xl bg-gradient-to-br from-[#2b1f1f] to-[#1a1212] border border-[#3d2727] relative overflow-hidden">
            {/* 装饰性背景光晕 */}
            <div className="absolute top-0 right-0 w-32 h-32 bg-red-500/10 rounded-full blur-3xl pointer-events-none"></div>

            <div className="flex justify-between items-end mb-3">
              <div>
                <h2 className="text-lg font-black text-[#ff4d4f] italic tracking-wide">🔥 正在热播</h2>
                <p className="text-xs text-[#ff4d4f]/70 mt-0.5">全网首播，不容错过</p>
              </div>
              <span className="text-xs text-[#ff4d4f] cursor-pointer hover:underline">查看更多 &gt;</span>
            </div>

            {/* 混合排版：左边一个大视频，右边两个小视频堆叠 */}
            {videos.length >= 3 && (
              <div className="grid grid-cols-2 gap-2 h-[200px]">
                {/* 左大图 */}
                <motion.div
                  className="relative rounded-lg overflow-hidden cursor-pointer"
                  whileTap={{ scale: 0.95 }}
                  onClick={() => navigate(`/video/${videos[0].id}`)}
                >
                  <img src={videos[0].coverUrl} alt={videos[0].title} className="w-full h-full object-cover" />
                  <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-2">
                    <span className="text-white text-sm font-bold truncate block">{videos[0].title}</span>
                  </div>
                </motion.div>

                {/* 右双图 */}
                <div className="flex flex-col gap-2">
                  {[videos[1], videos[2]].map((item, idx) => (
                    <motion.div
                      key={`special-${idx}`}
                      className="relative flex-1 rounded-lg overflow-hidden cursor-pointer bg-dark-card"
                      whileTap={{ scale: 0.95 }}
                      onClick={() => navigate(`/video/${item.id}`)}
                    >
                      <img src={item.coverUrl} alt={item.title} className="absolute inset-0 w-full h-full object-cover" />
                      <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-1.5">
                        <span className="text-white text-xs font-bold truncate block">{item.title}</span>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* 猜你在追 / 热门推荐 */}
          <div>
            <h2 className="text-lg font-bold mb-3 flex items-center text-white">
              <span>热门推荐</span>
            </h2>
            <div className="grid grid-cols-2 gap-3">
              {videos.map((item) => (
                <motion.div
                  key={item.id}
                  className="flex flex-col gap-1 rounded overflow-hidden cursor-pointer"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => navigate(`/video/${item.id}`)}
                >
                  <div className="relative aspect-[3/4] bg-dark-card rounded-lg overflow-hidden group">
                    <img src={item.coverUrl} alt={item.title} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />

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
                </motion.div>
              ))}
            </div>

            {/* 上拉加载状态 */}
            {isLoadingMore && (
              <div className="flex justify-center items-center h-12 text-xs text-dark-muted mt-4 gap-1">
                 <Loader2 size={14} className="animate-spin" /> 加载更多中...
              </div>
            )}
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default Home;
