import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { X, Smartphone } from 'lucide-react';
import useAuthStore from '@/store/auth';

export const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuthStore();
  const [phone, setPhone] = useState('13800138000');
  const [code, setCode] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [countdown, setCountdown] = useState(60);

  const handleSendCode = () => {
    if (phone.length !== 11) return alert('请输入正确的手机号');
    setIsSending(true);
    let timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          setIsSending(false);
          return 60;
        }
        return prev - 1;
      });
    }, 1000);
    alert('验证码已发送: 1234');
    setCode('1234'); // 自动填入以便测试
  };

  const handleLogin = () => {
    if (phone.length === 11 && code.length >= 4) {
      login({ id: '12345678', name: 'VIP用户', isVip: true, avatar: 'https://dummyimage.com/100x100/e8c081/333&text=VIP' });
      navigate(-1);
    } else {
      alert('请输入正确的手机号和验证码');
    }
  };

  return (
    <div className="w-full min-h-screen bg-dark-bg text-dark-text flex flex-col fixed inset-0 z-[100] animate-fade-in">
      <div className="p-4 flex justify-between items-center">
        <X size={24} className="text-white cursor-pointer" onClick={() => navigate(-1)} />
        <span className="text-sm text-dark-muted">帮助</span>
      </div>

      <div className="px-8 mt-10">
        <h1 className="text-2xl font-bold text-white mb-2">手机号快捷登录</h1>
        <p className="text-sm text-dark-muted mb-10">未注册的手机号验证后自动创建爱奇艺账号</p>

        <div className="flex flex-col gap-6">
          <div className="flex items-center border-b border-gray-700 pb-2">
            <span className="text-white text-lg font-medium mr-4">+86</span>
            <input
              type="tel"
              maxLength={11}
              className="flex-1 bg-transparent text-white text-lg outline-none placeholder:text-gray-600"
              placeholder="请输入手机号"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
            />
          </div>

          <div className="flex items-center border-b border-gray-700 pb-2">
            <input
              type="text"
              maxLength={6}
              className="flex-1 bg-transparent text-white text-lg outline-none placeholder:text-gray-600"
              placeholder="请输入验证码"
              value={code}
              onChange={(e) => setCode(e.target.value)}
            />
            <button
              className={`text-sm ${isSending ? 'text-gray-500' : 'text-brand'} font-medium`}
              onClick={handleSendCode}
              disabled={isSending}
            >
              {isSending ? `${countdown}s 后重新获取` : '获取验证码'}
            </button>
          </div>

          <button
            className={`w-full py-3 rounded-full text-base font-bold mt-6 transition-colors ${
              phone.length === 11 && code.length >= 4
                ? 'bg-brand text-black'
                : 'bg-gray-800 text-gray-500'
            }`}
            onClick={handleLogin}
          >
            登录/注册
          </button>
        </div>

        <div className="mt-8 text-center text-xs text-dark-muted">
          登录即代表同意 <span className="text-brand">《爱奇艺服务协议》</span> 和 <span className="text-brand">《隐私政策》</span>
        </div>

        <div className="absolute bottom-10 left-0 right-0 flex flex-col items-center">
          <span className="text-xs text-gray-500 mb-4">其他登录方式</span>
          <div className="flex gap-6">
            <div className="w-12 h-12 bg-gray-800 rounded-full flex items-center justify-center text-green-500">
              <Smartphone size={24} /> {/* 微信占位 */}
            </div>
            <div className="w-12 h-12 bg-gray-800 rounded-full flex items-center justify-center text-blue-400">
              <Smartphone size={24} /> {/* QQ占位 */}
            </div>
            <div className="w-12 h-12 bg-gray-800 rounded-full flex items-center justify-center text-white">
              <Smartphone size={24} /> {/* 苹果占位 */}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
