import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeft, Search as SearchIcon, X, Trash2, Flame } from 'lucide-react';

export const Search = () => {
  const navigate = useNavigate();
  const [keyword, setKeyword] = useState('');
  const [history, setHistory] = useState<string[]>([]);
  const [isSearching, setIsSearching] = useState(false);

  // 模拟热搜数据
  const hotSearches = [
    { title: '狂飙', index: 1, hot: true },
    { title: '三体', index: 2, hot: true },
    { title: '流浪地球2', index: 3, hot: false },
    { title: '苍兰诀', index: 4, hot: false },
    { title: '名侦探柯南', index: 5, hot: false },
  ];

  // 模拟搜索结果数据
  const mockResults = [
    { id: 'v1', title: '狂飙 电视剧全集在线观看', desc: '张译、张颂文主演的热播反黑剧。', cover: 'https://dummyimage.com/120x160/1f1f1f/fff&text=KB' },
    { id: 'v2', title: '狂飙 幕后花絮', desc: '看看张颂文是如何吃面条的。', cover: 'https://dummyimage.com/120x160/1f1f1f/fff&text=KBMH' },
  ];

  useEffect(() => {
    // 从本地存储加载搜索历史
    const saved = localStorage.getItem('search_history');
    if (saved) {
      try {
        setHistory(JSON.parse(saved));
      } catch (e) {
        console.error(e);
      }
    }
  }, []);

  const saveHistory = (newKeyword: string) => {
    if (!newKeyword.trim()) return;
    const newHistory = [newKeyword, ...history.filter(h => h !== newKeyword)].slice(0, 10);
    setHistory(newHistory);
    localStorage.setItem('search_history', JSON.stringify(newHistory));
  };

  const handleSearch = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!keyword.trim()) return;
    saveHistory(keyword);
    setIsSearching(true);
    // 这里如果做真实请求可以调用 api，这里只展示 mock 结果
  };

  const handleTagClick = (tag: string) => {
    setKeyword(tag);
    saveHistory(tag);
    setIsSearching(true);
  };

  const clearHistory = () => {
    setHistory([]);
    localStorage.removeItem('search_history');
  };

  return (
    <div className="w-full min-h-screen bg-[#121212] text-white flex flex-col">
      {/* 搜索框头部 */}
      <div className="flex items-center gap-3 p-4 bg-[#1f1f1f] sticky top-0 z-10">
        <button onClick={() => navigate(-1)} className="text-white">
          <ChevronLeft size={24} />
        </button>
        <form onSubmit={handleSearch} className="flex-1 flex items-center bg-black/40 rounded-full px-4 py-1.5 border border-gray-700 focus-within:border-[#00cc33] transition-colors">
          <SearchIcon size={16} className="text-gray-400" />
          <input
            type="text"
            placeholder="搜索全网影视、综艺、动漫"
            value={keyword}
            onChange={(e) => {
              setKeyword(e.target.value);
              if (!e.target.value) setIsSearching(false);
            }}
            className="flex-1 bg-transparent border-none outline-none px-2 text-sm text-white placeholder:text-gray-500"
            autoFocus
          />
          {keyword && (
            <button type="button" onClick={() => { setKeyword(''); setIsSearching(false); }} className="p-1">
              <X size={16} className="text-gray-400" />
            </button>
          )}
        </form>
        <button onClick={handleSearch} className="text-[#00cc33] font-bold text-sm whitespace-nowrap">
          搜索
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        {!isSearching ? (
          <>
            {/* 搜索历史 */}
            {history.length > 0 && (
              <div className="mb-6">
                <div className="flex justify-between items-center mb-3">
                  <h3 className="text-sm font-bold text-white/90">搜索历史</h3>
                  <button onClick={clearHistory}>
                    <Trash2 size={16} className="text-gray-500" />
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {history.map((item, idx) => (
                    <span
                      key={idx}
                      onClick={() => handleTagClick(item)}
                      className="bg-[#1f1f1f] text-gray-300 text-xs px-3 py-1.5 rounded-full cursor-pointer active:scale-95 transition-transform"
                    >
                      {item}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* 热门搜索 */}
            <div>
              <h3 className="text-sm font-bold text-white/90 mb-3 flex items-center gap-1">
                <Flame size={16} className="text-red-500" /> 爱奇艺热搜榜
              </h3>
              <div className="flex flex-col gap-4">
                {hotSearches.map((item) => (
                  <div
                    key={item.index}
                    onClick={() => handleTagClick(item.title)}
                    className="flex items-center gap-3 cursor-pointer active:opacity-70"
                  >
                    <span className={`text-sm font-bold italic w-5 ${item.index <= 3 ? 'text-red-500' : 'text-gray-500'}`}>
                      {item.index}
                    </span>
                    <span className="text-sm text-gray-200">{item.title}</span>
                    {item.hot && <span className="text-[10px] bg-red-500/20 text-red-500 px-1 rounded font-bold">HOT</span>}
                  </div>
                ))}
              </div>
            </div>
          </>
        ) : (
          /* 搜索结果页 (简易 Mock) */
          <div className="flex flex-col gap-4">
            <h3 className="text-xs text-gray-500 mb-2">为您找到 "{keyword}" 的相关结果</h3>
            {mockResults.map((item) => (
              <div key={item.id} className="flex gap-3 bg-[#1f1f1f] p-3 rounded-lg cursor-pointer" onClick={() => navigate(`/video/${item.id}`)}>
                <img src={item.cover} alt="cover" className="w-24 h-32 object-cover rounded" />
                <div className="flex flex-col gap-2 flex-1">
                  <h4 className="text-sm font-bold text-white">{item.title}</h4>
                  <p className="text-xs text-gray-400 line-clamp-2">{item.desc}</p>
                  <button className="mt-auto self-start border border-[#00cc33] text-[#00cc33] text-xs px-4 py-1 rounded-full">
                    立即播放
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Search;
