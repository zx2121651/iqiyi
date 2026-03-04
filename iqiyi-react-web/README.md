# 爱奇艺高仿前端 Web 原型 (iqiyi-react-web)

这是使用 Vite + React + TypeScript + TailwindCSS 开发的爱奇艺 Web 端前端原型项目。
本项目旨在为同名 uni-app x 移动端应用提供 UI/UX 的参考基准。

## 技术栈
- 框架: React 18, Vite
- 语言: TypeScript
- 样式: TailwindCSS
- 路由: react-router-dom v6
- 状态管理: Zustand
- 图标: lucide-react
- Mock数据: mockjs

## 目录结构
```text
src/
  assets/     # 静态资源 (图片、字体)
  components/ # 可复用的基础 UI 组件 (如 Layout, Button 等)
  hooks/      # 自定义 React Hooks
  mock/       # 本地 Mock 数据配置
  pages/      # 页面级组件 (首页, 随刻, 会员, 我的)
  router/     # 前端路由配置
  store/      # Zustand 全局状态仓库
  styles/     # 全局 CSS 样式 (Tailwind 配置)
  utils/      # 通用工具函数 (如网络请求封装等)
```

## 运行项目

确保你已安装 Node.js，并在 `iqiyi-react-web` 目录下执行：

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

浏览器会自动打开 `http://localhost:3000` 预览页面。

## 页面规划
- **首页**: 包含轮播图、频道分类、猜你喜欢、热门推荐流。
- **随刻 (短视频)**: 仿抖音上下滑动切换短视频。
- **会员**: 会员权益展示、VIP专享内容推荐。
- **我的**: 用户信息、播放历史、收藏、设置。
