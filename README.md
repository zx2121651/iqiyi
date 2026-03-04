# 高仿爱奇艺视频 App 跨端项目 (iQiyi Clone)

本项目是一个跨平台的高保真视频应用开发骨架。包含了两个完全独立的项目工程，旨在探索 **Web 原型快速验证** 与 **移动端原生高性能渲染 (uni-app x)** 保持 UI 和交互一致性的最佳实践。

## 项目结构概览

为了实现跨端开发的完整体验，本仓库被明确划分为两个子项目：

1. **`iqiyi-react-web/` (React Web 前端原型)**
   - **定位**: 快速原型验证、PC端展示、H5 页面。
   - **技术栈**: Vite + React 18 + TypeScript + TailwindCSS + Zustand + React Router v6。
   - **特点**: 开发效率极高，利用 TailwindCSS 快速实现复杂的 UI 布局和动画，采用 Web 标准实现。
   - **文档**: [iqiyi-react-web/README.md](./iqiyi-react-web/README.md)

2. **`iqiyi-uniappx/` (uni-app x 原生移动端应用)**
   - **定位**: Android / iOS 原生 App。
   - **技术栈**: uni-app x (基于 Vue3 + UTS)。
   - **特点**: 使用 UTS (Uni TypeScript) 编译为原生代码 (Kotlin/Swift)，不依赖 WebView，具备极高的运行性能和流畅的原生动画体验。样式上遵循严格的 Flex 布局。
   - **文档**: [iqiyi-uniappx/README.md](./iqiyi-uniappx/README.md)

## 核心功能规划 (Roadmap)

我们采用了“**先搭框架，增量开发**”的策略。以下是初期和后期的核心功能：

### 第一阶段：基础框架 (当前阶段 - 已完成)
- [x] 清空历史无效代码。
- [x] 分别建立 React Web 和 uni-app x 工程骨架。
- [x] 实现一致的深色主题 (Dark Theme) 视觉风格。
- [x] 实现跨端一致的底层路由和底部导航栏 (TabBar)：
  - **首页**: 包含轮播、推荐内容排版。
  - **随刻**: 短视频沉浸式全屏流。
  - **会员**: 特权和 VIP 专享影视。
  - **我的**: 个人资料、历史记录等。
- [x] 提供详细的中英文文档和代码注释。

### 第二阶段：核心组件与 Mock 数据 (待开发)
- [ ] 封装公用 UI 组件：视频卡片、轮播图 (Swiper)、自定义播放器容器。
- [ ] 在两个项目中分别配置 Mock 数据源 (基于 `mockjs` / 本地 JSON)。
- [ ] 填充完整的首页数据流和短视频信息流。
- [ ] 增加下拉刷新、上拉加载更多功能。

### 第三阶段：真实交互与动画 (待开发)
- [ ] **React Web**: 使用 `framer-motion` 增强路由切换和 UI 交互的微动画。
- [ ] **uni-app x**: 使用原生 API (`uni.createAnimation` 或 UTS 动画绑定) 还原 Web 端的动画效果。
- [ ] 真实的前后端 API 对接 (如有)。

## 运行说明

本仓库本身只是一个父级目录，请**分别进入各自的子目录**按照文档运行对应的项目。

- 若要运行 Web 原型：
  ```bash
  cd iqiyi-react-web
  npm install
  npm run dev
  ```
- 若要运行移动端 App，请使用 HBuilderX 打开 `iqiyi-uniappx` 目录并运行至手机或模拟器。

## 开发规范与约定

1. **统一的 UI 设计语言**: 由于涉及两套技术栈，必须保持 CSS 变量 (如：`#121212` 暗色背景, `#00cc33` 爱奇艺绿品牌色) 的高度一致。
2. **注释清晰**: 各个模块必须带有清晰的中文注释，说明该文件或组件的核心功能，特别是状态管理和路由部分。
3. **Mock 优先**: 接口对接前，必须先在 `mock` 目录下定义好数据结构，确保视图开发不受后端阻塞。

---

*由 Jules 开发与维护*
