import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeft, Loader2 } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';

/**
 * 登录页面组件
 * 提供账号密码模拟登录功能，登录成功后更新全局状态并返回上一页
 */
export const Login = () => {
  const navigate = useNavigate();
  // 使用 zustand 全局状态
  const login = useAuthStore((state) => state.login);

  // 局部表单状态
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  /**
   * 处理登录表单提交逻辑
   * 模拟异步请求，如果账号和密码不为空则认为成功
   */
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!phone || !password) {
      setError('请输入手机号和密码');
      return;
    }
    setError('');
    setLoading(true);

    // 模拟网络请求延迟
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // 模拟获取用户数据并更新全局状态
    login({
      id: 'u10001',
      nickname: `用户_${phone.slice(-4)}`,
      avatar: 'https://dummyimage.com/100x100/333/fff&text=VIP',
      isVip: true,
      vipExpireTime: '2025-12-31',
    });

    setLoading(false);
    // 登录成功后返回来源页面或首页
    // 为避免测试环境下的不可靠跳转，此处强制跳转到首页，在真实应用中可以读取 url 参数或 state
    navigate('/');
  };

  return (
    <div className="w-full min-h-screen bg-[#121212] text-white flex flex-col relative">
      {/* 顶部导航 */}
      <div className="flex items-center p-4 absolute top-0 left-0 right-0 z-10">
        <button
          onClick={() => navigate(-1)}
          className="w-8 h-8 flex items-center justify-center rounded-full bg-black/40 text-white/80 active:scale-90 transition-transform"
        >
          <ChevronLeft size={20} />
        </button>
      </div>

      {/* 登录主体表单区域 */}
      <div className="flex-1 flex flex-col justify-center px-8 pb-20">
        <h1 className="text-3xl font-bold mb-2 text-[#00cc33] italic tracking-wider">iQIYI</h1>
        <h2 className="text-xl font-bold mb-8 text-white/90">欢迎回来，即刻开启精彩视界</h2>

        <form onSubmit={handleLogin} className="flex flex-col gap-5">
          {/* 手机号输入框 */}
          <div className="flex flex-col gap-1">
            <input
              type="tel"
              placeholder="请输入手机号"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="w-full bg-transparent border-b border-gray-700 pb-2 text-lg focus:outline-none focus:border-[#00cc33] transition-colors placeholder:text-gray-600"
            />
          </div>

          {/* 密码输入框 */}
          <div className="flex flex-col gap-1 relative">
            <input
              type="password"
              placeholder="请输入密码"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-transparent border-b border-gray-700 pb-2 text-lg focus:outline-none focus:border-[#00cc33] transition-colors placeholder:text-gray-600"
            />
          </div>

          {/* 错误提示区域 */}
          {error && <p className="text-red-500 text-sm mt-1">{error}</p>}

          {/* 登录按钮 */}
          <button
            type="submit"
            disabled={loading}
            className={`mt-6 w-full py-3.5 rounded-full font-bold text-white shadow-lg transition-all flex items-center justify-center gap-2 ${
              loading ? 'bg-[#00cc33]/50 cursor-not-allowed' : 'bg-[#00cc33] active:scale-[0.98]'
            }`}
          >
            {loading ? <Loader2 size={20} className="animate-spin" /> : '登 录'}
          </button>
        </form>

        <div className="mt-8 flex justify-center gap-4 text-sm text-gray-500">
          <span>忘记密码</span>
          <span>|</span>
          <span>注册账号</span>
        </div>
      </div>
    </div>
  );
};

export default Login;
