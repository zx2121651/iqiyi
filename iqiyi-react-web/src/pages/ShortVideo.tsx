import React from 'react';

/**
 * 随刻 (短视频) 页面组件
 * 展示类似抖音、快手的短视频流
 */
export const ShortVideo = () => {
  return (
    <div className="flex h-screen w-full flex-col items-center justify-center animate-fade-in bg-black pb-16">
      <h1 className="text-2xl font-bold text-white mb-4">短视频流</h1>
      <p className="text-dark-muted">上滑查看更多短视频 (待开发)</p>
    </div>
  );
};

export default ShortVideo;
