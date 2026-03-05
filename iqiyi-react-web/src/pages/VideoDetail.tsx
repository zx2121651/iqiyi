import React, { useEffect, useState } from 'react';
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

export const VideoDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [detail, setDetail] = useState<VideoDetailData | null>(null);
  const [related, setRelated] = useState<RelatedVideo[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [detailData, relatedData] = await Promise.all([
          request.get<any, VideoDetailData>(`/video/detail?id=${id || '1'}`),
          request.get<any, RelatedVideo[]>('/video/related'),
        ]);
        setDetail(detailData);
        setRelated(relatedData);
      } catch (error) {
        console.error('Failed to load video detail:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

  const formatCount = (count: number) => {
    if (count > 10000) return (count / 10000).toFixed(1) + 'w';
    return count.toString();
  };

  if (loading || !detail) {
    return <div className="flex h-screen w-full items-center justify-center bg-[#121212] text-white">加载中...</div>;
  }

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
      <div className="w-full aspect-video bg-black sticky top-0 z-40">
        <video
          src={detail.playUrl}
          poster={detail.coverUrl}
          controls
          autoPlay
          playsInline
          className="w-full h-full object-contain"
        >
          您的浏览器不支持 video 标签。
        </video>
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
