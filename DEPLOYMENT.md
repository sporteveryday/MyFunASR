# FunASR 语音识别系统

基于阿里 FunASR 框架的语音识别 Web 应用。

## 功能特性

- 🎤 支持音频/视频文件上传转写
- 🔗 支持视频链接解析（YouTube、Bilibili 等）
- 🌐 多语言自动识别（中/英/日/韩/粤）
- 🎬 视频嵌入预览播放
- 📋 一键复制识别结果

## 快速开始

### 本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动 API 服务
python funasr_api_server.py

# 3. 打开浏览器访问
# file:///path/to/web/index.html
```

### Docker 部署

```bash
# 使用 docker-compose
docker-compose up -d

# 或手动构建
docker build -t funasr-api .
docker run -d --gpus all -p 8000:8000 funasr-api
```

### Vercel 部署（前端）

```bash
cd web
vercel --prod
```

## API 文档

启动服务后访问：http://localhost:8000/docs

### 主要端点

| 端点              | 方法 | 说明     |
| ----------------- | ---- | -------- |
| `/transcribe`     | POST | 文件转写 |
| `/transcribe_url` | POST | URL 转写 |
| `/health`         | GET  | 健康检查 |

## 技术栈

- **后端**: Python, FastAPI, FunASR, SenseVoiceSmall
- **前端**: Vue 3, HTML5, CSS3
- **部署**: Docker, Vercel

## 许可证

MIT License
