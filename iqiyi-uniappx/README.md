# 爱奇艺高仿移动端 App (iqiyi-uniappx)

这是使用 uni-app x (基于 Vue3 和 UTS) 开发的高仿爱奇艺视频 App 项目。
本项目专注于移动端（Android / iOS）体验，UI 和动画效果旨在与 Web 原型保持高度一致。

## 技术栈
- 框架: uni-app x
- 核心语言: UTS (兼容 TypeScript)、Vue3
- 样式: 原生 CSS / Flex 布局
- 状态管理: Pinia
- 页面配置: `pages.json`
- 底部导航: 原生 TabBar

## 目录结构
```text
components/  # 全局可复用的自定义组件 (UTS 开发)
mock/        # 离线/开发环境下的模拟数据
pages/       # 业务页面 (按照原生路由规范配置)
static/      # 静态资源 (图片、本地 icon 等)
store/       # Pinia 状态管理
utils/       # 通用 UTS 工具函数
App.uvue     # 应用生命周期及全局样式入口
manifest.json# 应用配置 (包含 AppID, 权限, 编译等配置)
pages.json   # 页面路由及底部 TabBar 配置
```

## 开发与运行

1. 下载并安装 [HBuilderX (支持 uni-app x 版)](https://www.dcloud.io/hbuilderx.html)。
2. 在 HBuilderX 中打开 `iqiyi-uniappx` 目录。
3. 点击顶部菜单栏的 **运行** -> **运行到内置模拟器 / 手机真机运行** 即可进行编译和调试。

> **注意：** uni-app x 是一套原生渲染方案，CSS 支持仅限于 Flex 布局和部分样式，不可使用针对浏览器的特定 DOM 或 CSS3 属性，请严格按照 UTS 和原生渲染规范进行开发。
