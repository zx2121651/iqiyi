import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeft, Search as SearchIcon, X, Clock, Flame } from 'lucide-react';
import { motion } from 'framer-motion';

export const Search = () => {
  const navigate = useNavigate();
  const [keyword, setKeyword] = useState('');
  const [history, setHistory] = useState<string[]>(['狂飙', '流浪地球2', '种地吧']);

  const hotSearches = [
    { id: 1, text: '三体', isHot: true },
    { id: 2, text: '长风渡', isHot: true },
    { id: 3, text: '莲花楼', isHot: false },
    { id: 4, text: '中国说唱巅峰对决', isHot: false },
    { id: 5, text: '显微镜下的大明', isHot: false },
    { id: 6, text: '独行月球', isHot: false },
  ];

  const handleSearch = (text: string) => {
    if (!text.trim()) return;
    // 模拟搜索跳转行为
    alert(`搜索: ${text}`);
    if (!history.includes(text)) {
      setHistory([text, ...history].slice(0, 10)); // 保留最近10条
    }
  };

  const clearHistory = () => {
    setHistory([]);
  };

  return (
    <div className="w-full min-h-screen bg-dark-bg text-dark-text flex flex-col">
      {/* 搜索头部 */}
      <div className="flex items-center gap-3 px-4 py-3 bg-dark-card sticky top-0 z-50">
        <ChevronLeft size={24} className="text-white cursor-pointer" onClick={() => navigate(-1)} />
        <div className="flex-1 flex items-center bg-[#2a2a2a] rounded-full px-3 py-1.5 border border-white/10">
          <SearchIcon size={16} className="text-dark-muted" />
          <input
            type="text"
            className="flex-1 bg-transparent border-none outline-none text-white text-sm px-2 placeholder:text-dark-muted"
            placeholder="搜索你想看的影视综"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleSearch(keyword);
            }}
            autoFocus
          />
          {keyword && (
            <X size={16} className="text-dark-muted cursor-pointer" onClick={() => setKeyword('')} />
          )}
        </div>
        <span className="text-sm font-medium text-white cursor-pointer" onClick={() => handleSearch(keyword)}>
          搜索
        </span>
      </div>

      <div className="p-4 flex-1 overflow-y-auto">
        {/* 搜索历史 */}
        {history.length > 0 && (
          <div className="mb-6">
            <div className="flex justify-between items-center mb-3">
              <h3 className="text-sm font-bold text-white/90">搜索历史</h3>
              <span className="text-xs text-dark-muted cursor-pointer flex items-center gap-1" onClick={clearHistory}>
                清除
              </span>
            </div>
            <div className="flex flex-wrap gap-2">
              {history.map((item, index) => (
                <motion.div
                  key={index}
                  whileTap={{ scale: 0.95 }}
                  className="bg-[#2a2a2a] text-xs text-white/80 px-3 py-1.5 rounded-full cursor-pointer flex items-center gap-1"
                  onClick={() => {
                    setKeyword(item);
                    handleSearch(item);
                  }}
                >
                  <Clock size={12} className="text-dark-muted" />
                  {item}
                </motion.div>
              ))}
            </div>
          </div>
        )}

        {/* 猜你想搜 / 热搜榜 */}
        <div>
          <h3 className="text-sm font-bold text-white/90 mb-3 flex items-center gap-1">
            <Flame size={16} className="text-red-500" /> 爱奇艺热搜榜
          </h3>
          <div className="flex flex-col gap-4">
            {hotSearches.map((item, index) => (
              <div
                key={item.id}
                className="flex items-center gap-3 cursor-pointer group"
                onClick={() => {
                  setKeyword(item.text);
                  handleSearch(item.text);
                }}
              >
                <span className={`text-sm font-bold w-4 text-center ${index < 3 ? 'text-red-500' : 'text-dark-muted'}`}>
                  {index + 1}
                </span>
                <span className="text-sm text-white/90 group-hover:text-brand transition-colors flex-1 truncate">
                  {item.text}
                </span>
                {item.isHot && (
                  <span className="text-[10px] bg-red-500/20 text-red-500 px-1 rounded font-bold">HOT</span>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Search;
