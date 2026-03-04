import React from 'react';

/**
 * 首页组件
 * 提供推荐的视频流、横幅等
 */
export const Home = () => {
  return (
    <div className="p-4 flex flex-col gap-4 animate-fade-in pb-20">
      <h1 className="text-2xl font-bold">首页推荐</h1>
      <div className="h-40 bg-dark-card rounded-lg flex items-center justify-center text-dark-muted">
        Banner 区域 (待开发)
      </div>
      <div className="grid grid-cols-2 gap-3">
        {[1, 2, 3, 4, 5, 6].map((item) => (
          <div key={item} className="h-32 bg-dark-card rounded flex items-center justify-center text-dark-muted text-sm">
            视频卡片 {item}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;
