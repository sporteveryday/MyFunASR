# FunASR Web - Vue 3 + Vite

现代化的语音识别 Web 应用，基于 Vue 3 和 Vite 构建。

## 特性

- 📁 **文件上传** - 支持拖拽上传音频/视频文件
- 🔗 **URL 转录** - 支持 YouTube、Bilibili 等平台视频链接
- 🎵 **媒体预览** - 实时预览视频和音频
- ⚙️ **灵活配置** - 自定义 API 服务器地址
- 🌙 **暗色主题** - 现代化的 UI 设计
- 📱 **响应式** - 完美适配移动端

## 快速开始

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:5173/

### 构建生产版本

```bash
npm run build
```

## 支持的格式

### 音频

WAV, MP3, M4A, FLAC, AAC, OGG, WMA

### 视频

MP4, AVI, MKV, MOV, WMV, FLV, WebM

## 配置

### API 服务器

点击右上角的设置按钮配置后端 API 地址。默认地址为 `http://localhost:8000`

## 项目结构

```
src/
├── components/       # Vue 组件
├── composables/      # 可复用逻辑
├── utils/            # 工具函数
├── assets/           # 静态资源
├── App.vue           # 主应用
└── main.js           # 入口文件
```

## 技术栈

- Vue 3
- Vite
- JavaScript (ES6+)

## License

MIT
