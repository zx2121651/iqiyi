import axios from 'axios';

// 创建通用的 axios 实例
const request = axios.create({
  baseURL: '/api', // 这里对应 vite-plugin-mock 的配置
  timeout: 5000,
});

// 响应拦截器：统一处理返回的格式
request.interceptors.response.use(
  (response) => {
    // 假设后端返回的数据结构总是 { code: 200, message: "...", data: [...] }
    if (response.data.code === 200) {
      return response.data.data;
    }
    return Promise.reject(new Error(response.data.message || 'Error'));
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default request;
