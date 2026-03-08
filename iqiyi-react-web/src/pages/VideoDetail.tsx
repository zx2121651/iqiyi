import { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import request from '@/utils/request';
import { ChevronLeft, Share2, Heart, Star, Download, MessageSquare } from 'lucide-react';

interface VideoDetailData {
  id: string;
  title: string;
  playUrl: string;
  coverUrl: string;
  score: number;
  playCount: number;
  year: string;
  tags: string[];
  desc: string;
  likeCount: number;
  commentCount: number;
}

interface RelatedVideo {
  id: string;
  title: string;
  coverUrl: string;
  playCount: number;
  duration: string;
}

/**
 * 视频详情页面组件
 * 包含：播放器、视频信息展示、操作按钮、评论区及更多相关推荐
 */
export const VideoDetail = () => {
  // 从路由参数中获取视频 id
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  // 详情数据和推荐列表状态
  const [detail, setDetail] = useState<VideoDetailData | null>(null);
  const [related, setRelated] = useState<RelatedVideo[]>([]);
  const [loading, setLoading] = useState(true);

  /**
   * 初始化数据请求
   * 当 id 发生变化时，请求新的视频详情及相关推荐数据
   */
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        // 并发请求视频详情及相关视频列表
        const [detailData, relatedData] = await Promise.all([
          request.get<any, VideoDetailData>(`/video/detail?id=${id || '1'}`),
          request.get<any, RelatedVideo[]>('/video/related'),
        ]);
        setDetail(detailData);
        setRelated(relatedData);
      } catch (error) {
        console.error('获取视频详情失败:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

  /**
   * 格式化数量显示（将超万数字转为带 "w" 的格式）
   */
  const formatCount = (count: number) => {
    if (count > 10000) return (count / 10000).toFixed(1) + 'w';
    return count.toString();
  };

  // 如果处于加载中或详情未加载，则显示加载提示
  if (loading || !detail) {
    return <div className="flex h-screen w-full items-center justify-center bg-[#121212] text-white">加载中...</div>;
  }

  // 模拟评论数据
  const [comments] = useState([
    { id: 1, user: '用户A', avatar: 'https://dummyimage.com/100x100/333/fff&text=A', content: '这个视频拍得太好了！', time: '2小时前' },
    { id: 2, user: '用户B', avatar: 'https://dummyimage.com/100x100/444/fff&text=B', content: '剧情很紧凑，推荐大家看。', time: '5小时前' },
    { id: 3, user: '用户C', avatar: 'https://dummyimage.com/100x100/555/fff&text=C', content: '绝了绝了，一口气看完！', time: '1天前' },
  ]);

  // 模拟弹幕数据源
  const [danmakuList] = useState([
    { text: '前方高能', time: 2, color: '#ff0000' },
    { text: '绝了', time: 4, color: '#ffffff' },
    { text: '哈哈哈哈哈', time: 5, color: '#ffff00' },
    { text: '这段演技炸裂', time: 8, color: '#ffffff' },
    { text: '来了来了', time: 1, color: '#ffffff' },
  ]);

  // 用于获取视频元素，以便读取 currentTime 控制弹幕
  const videoRef = useRef<HTMLVideoElement>(null);
  // 当前正在屏幕上展示的弹幕列表状态
  const [currentDanmaku, setCurrentDanmaku] = useState<{text:string, color:string, top:number, id:number}[]>([]);

  /**
   * 简易弹幕逻辑实现
   * 通过定时器监听视频当前播放时间，筛选出需要显示的弹幕进行挂载
   */
  useEffect(() => {
    let interval: any;
    // 只有在视频元素就绪，且未处于加载中状态时，开启定时器
    if (videoRef.current && !loading && detail) {
      interval = setInterval(() => {
        // 如果视频不存在或处于暂停状态，则不触发弹幕
        if (!videoRef.current || videoRef.current.paused) return;

        const time = Math.floor(videoRef.current.currentTime);
        // 查找属于当前秒的弹幕，附加随机垂直位置与唯一ID
        const newDanmaku = danmakuList.filter(d => d.time === time).map((d, i) => ({
          ...d,
          top: Math.random() * 60 + 10, // 垂直位置随机 10% ~ 70%
          id: Date.now() + i
        }));

        if (newDanmaku.length > 0) {
          // 追加新的弹幕节点
          setCurrentDanmaku(prev => [...prev, ...newDanmaku]);
          // 4 秒后（动画执行完毕后），自动清理这些弹幕节点避免 DOM 臃肿
          setTimeout(() => {
             setCurrentDanmaku(prev => prev.filter(p => !newDanmaku.find(n => n.id === p.id)));
          }, 4000);
        }
      }, 1000); // 每秒检查一次
    }
    // 卸载组件时清理定时器
    return () => clearInterval(interval);
  }, [danmakuList, loading, detail]);

  return (
    <div className="w-full min-h-screen bg-[#121212] text-dark-text pb-6">
      {/* 顶部固定导航条 (悬浮在视频上方或视频上方留出空间) */}
      <div className="fixed top-0 left-0 right-0 h-12 z-50 flex items-center px-4 bg-gradient-to-b from-black/80 to-transparent pointer-events-none">
        <div
          className="w-8 h-8 rounded-full bg-black/40 flex items-center justify-center pointer-events-auto cursor-pointer"
          onClick={() => navigate(-1)}
        >
          <ChevronLeft size={20} color="white" />
        </div>
      </div>

      {/* 视频播放器区域 (固定 16:9 比例) */}
      <div className="w-full aspect-video bg-black sticky top-0 z-40 relative overflow-hidden">
        <video
          ref={videoRef}
          src="https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4"
          poster={detail.coverUrl}
          controls
          autoPlay
          playsInline
          className="w-full h-full object-contain relative z-10"
        >
          您的浏览器不支持 video 标签。
        </video>

        {/* 弹幕层 */}
        <div className="absolute inset-0 pointer-events-none z-20 overflow-hidden">
          {currentDanmaku.map((item) => (
            <div
              key={item.id}
              className="absolute whitespace-nowrap text-sm font-bold shadow-sm"
              style={{
                color: item.color,
                top: `${item.top}%`,
                animation: `danmakuMove 4s linear forwards`,
                right: '-100%',
              }}
            >
              {item.text}
            </div>
          ))}
          <style>{`
            @keyframes danmakuMove {
              0% { right: -100%; transform: translateX(100%); }
              100% { right: 100%; transform: translateX(-100%); }
            }
          `}</style>
        </div>
      </div>

      {/* 视频详情区域 */}
      <div className="p-4">
        <h1 className="text-xl font-bold leading-tight mb-2 text-white/90">{detail.title}</h1>

        <div className="flex items-center gap-3 text-xs text-dark-muted mb-4 font-medium">
          <span className="text-brand font-bold text-sm">{detail.score}分</span>
          <span>{detail.year}</span>
          <span>{formatCount(detail.playCount)}次播放</span>
        </div>

        {/* 标签 */}
        <div className="flex flex-wrap gap-2 mb-4">
          {detail.tags.map((tag, idx) => (
            <span key={idx} className="bg-[#1f1f1f] text-dark-muted px-2 py-0.5 rounded text-xs">
              {tag}
            </span>
          ))}
        </div>

        {/* 简介 (折叠/展开效果可后续实现，此处直接展示) */}
        <p className="text-sm text-dark-muted leading-relaxed line-clamp-2 mb-6">
          {detail.desc}
        </p>

        {/* 操作区 (点赞/收藏/下载/分享) */}
        <div className="flex justify-between items-center bg-[#1f1f1f] rounded-xl p-3 mb-6 shadow-sm">
          <div className="flex flex-col items-center gap-1 cursor-pointer">
            <Heart size={20} className="text-white/80" />
            <span className="text-[10px] text-dark-muted">{formatCount(detail.likeCount)}</span>
          </div>
          <div className="flex flex-col items-center gap-1 cursor-pointer">
            <Star size={20} className="text-white/80" />
            <span className="text-[10px] text-dark-muted">收藏</span>
          </div>
          <div className="flex flex-col items-center gap-1 cursor-pointer">
            <Download size={20} className="text-white/80" />
            <span className="text-[10px] text-dark-muted">下载</span>
          </div>
          <div className="flex flex-col items-center gap-1 cursor-pointer">
            <MessageSquare size={20} className="text-white/80" />
            <span className="text-[10px] text-dark-muted">{formatCount(detail.commentCount)}</span>
          </div>
          <div className="flex flex-col items-center gap-1 cursor-pointer">
            <Share2 size={20} className="text-white/80" />
            <span className="text-[10px] text-dark-muted">分享</span>
          </div>
        </div>

        {/* 评论区 */}
        <div className="mb-6">
          <h3 className="text-base font-bold mb-3 text-white/90">精彩评论 ({formatCount(detail.commentCount)})</h3>
          <div className="flex flex-col gap-4">
            {comments.map((comment) => (
              <div key={comment.id} className="flex gap-3">
                <img src={comment.avatar} alt="avatar" className="w-8 h-8 rounded-full flex-shrink-0" />
                <div className="flex flex-col flex-1 border-b border-gray-800 pb-3">
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-xs text-dark-muted font-medium">{comment.user}</span>
                    <span className="text-[10px] text-dark-muted">{comment.time}</span>
                  </div>
                  <p className="text-sm text-white/90">{comment.content}</p>
                  <div className="flex items-center gap-4 mt-2">
                    <span className="text-[10px] text-dark-muted flex items-center gap-1 cursor-pointer"><Heart size={12} /> 点赞</span>
                    <span className="text-[10px] text-dark-muted flex items-center gap-1 cursor-pointer"><MessageSquare size={12} /> 回复</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 更多推荐列表 */}
        <div>
          <h3 className="text-base font-bold mb-3 text-white/90">更多推荐</h3>
          <div className="flex flex-col gap-3">
            {related.map((item) => (
              <div
                key={item.id}
                className="flex gap-3 h-20 active:opacity-70 transition-opacity cursor-pointer"
                onClick={() => navigate(`/video/${item.id}`)}
              >
                {/* 左侧封面 16:9 */}
                <div className="relative h-full aspect-video bg-[#1f1f1f] rounded-lg overflow-hidden shrink-0">
                  <img src={item.coverUrl} alt={item.title} className="w-full h-full object-cover" />
                  <span className="absolute bottom-1 right-1 bg-black/70 text-white text-[10px] px-1 rounded">
                    {item.duration}
                  </span>
                </div>
                {/* 右侧信息 */}
                <div className="flex flex-col justify-between py-1 flex-1 min-w-0">
                  <h4 className="text-sm font-medium text-white/90 line-clamp-2 leading-tight">{item.title}</h4>
                  <div className="text-xs text-dark-muted">
                    {formatCount(item.playCount)}次播放
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
};

export default VideoDetail;
