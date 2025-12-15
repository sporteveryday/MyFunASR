#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FunASR API Server
提供语音/视频转文字的 REST API 服务

启动方式: python funasr_api_server.py
API 文档: http://localhost:8000/docs
"""

import os
import sys
import time
import tempfile
import logging
from pathlib import Path
from typing import Optional

import torch
import numpy as np
import soundfile as sf

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# 添加源码路径
sys.path.insert(0, str(Path(__file__).parent))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 支持的音频格式
AUDIO_EXTENSIONS = {'.wav', '.mp3', '.m4a', '.flac', '.aac', '.ogg', '.wma'}
# 支持的视频格式
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'}

# 全局模型缓存
_model_cache = {}


def get_model():
    """获取或初始化模型（懒加载）"""
    if 'model' not in _model_cache:
        logger.info("首次加载模型，请稍候...")
        
        # 导入并注册模型
        import importlib
        import pkgutil
        
        def import_submodules(package_name):
            package = importlib.import_module(package_name)
            for loader, name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                try:
                    importlib.import_module(name)
                except:
                    pass
        
        import_submodules("funasr.models")
        import_submodules("funasr.frontends")
        
        from funasr import AutoModel
        
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        logger.info(f"使用设备: {device}")
        
        # 使用 SenseVoiceSmall - 阿里最新最强模型
        # 特点：速度快5-10倍，精度高，支持多语言+情感识别+事件检测
        model = AutoModel(
            model="iic/SenseVoiceSmall",
            vad_model="fsmn-vad",
            vad_kwargs={"max_single_segment_time": 30000},
            device=device,
            disable_update=True,
        )
        
        _model_cache['model'] = model
        _model_cache['device'] = device
        _model_cache['model_name'] = 'SenseVoiceSmall'
        logger.info("SenseVoiceSmall 模型加载完成！")
    
    return _model_cache['model']


def extract_audio_from_video(video_path: str, output_path: str) -> bool:
    """从视频文件中提取音频"""
    try:
        from moviepy import VideoFileClip
        
        video = VideoFileClip(video_path)
        audio = video.audio
        
        if audio is None:
            logger.warning("视频文件没有音频轨道")
            return False
        
        # 导出为 wav 格式
        audio.write_audiofile(output_path, fps=16000, nbytes=2, codec='pcm_s16le', logger=None)
        video.close()
        return True
    except Exception as e:
        logger.error(f"提取音频失败: {e}")
        return False


def load_audio(file_path: str) -> tuple:
    """加载音频文件并返回音频数据和采样率"""
    import os
    import tempfile
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    # 需要转换的格式
    convert_formats = {'.m4a', '.mp3', '.aac', '.ogg', '.wma', '.flac'}
    
    try:
        # 如果是需要转换的格式，先用 ffmpeg 转为 wav
        if file_ext in convert_formats:
            try:
                import subprocess
                import imageio_ffmpeg
                
                ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
                logger.info(f"转换音频格式: {file_ext} -> wav (使用 ffmpeg)")
                
                # 创建临时 wav 文件
                temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
                temp_wav.close()
                
                # 使用 ffmpeg 转换
                cmd = [
                    ffmpeg_path,
                    '-y',  # 覆盖输出
                    '-i', file_path,
                    '-ar', '16000',  # 采样率
                    '-ac', '1',  # 单声道
                    '-f', 'wav',
                    temp_wav.name
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    file_path = temp_wav.name
                    logger.info("音频格式转换成功")
                else:
                    logger.warning(f"ffmpeg 转换失败: {result.stderr}")
                    
            except Exception as e:
                logger.warning(f"ffmpeg 转换失败，尝试使用 soundfile: {e}")
        
        # 使用 soundfile 读取
        audio_data, sample_rate = sf.read(file_path)
        
        # 如果是多通道，转为单通道
        if len(audio_data.shape) > 1:
            audio_data = audio_data.mean(axis=1)
        
        # 如果采样率不是16000，重采样
        if sample_rate != 16000:
            import librosa
            audio_data = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=16000)
            sample_rate = 16000
        
        # 确保是 float32
        audio_data = audio_data.astype(np.float32)
        
        duration = len(audio_data) / sample_rate
        return audio_data, sample_rate, duration
        
    except Exception as e:
        logger.error(f"加载音频失败: {e}")
        raise


def download_audio_from_url(url: str, output_dir: str) -> dict:
    """从视频链接下载音频"""
    import yt_dlp
    import imageio_ffmpeg
    import subprocess
    
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    logger.info(f"使用 ffmpeg: {ffmpeg_path}")
    
    temp_audio = os.path.join(output_dir, 'temp_audio')
    output_wav = os.path.join(output_dir, 'audio.wav')
    
    # 下载音频（不使用后处理器）
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': temp_audio + '.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            
            # 找到下载的文件
            downloaded_file = None
            for f in os.listdir(output_dir):
                if f.startswith('temp_audio') and not f.endswith('.wav'):
                    downloaded_file = os.path.join(output_dir, f)
                    break
            
            if not downloaded_file:
                raise Exception("未找到下载的音频文件")
            
            logger.info(f"下载完成: {downloaded_file}")
            
            # 使用 ffmpeg 转换为 wav
            logger.info("转换音频格式为 wav...")
            cmd = [
                ffmpeg_path,
                '-y',
                '-i', downloaded_file,
                '-ar', '16000',
                '-ac', '1',
                '-f', 'wav',
                output_wav
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"ffmpeg 转换失败: {result.stderr}")
                raise Exception(f"音频转换失败: {result.stderr}")
            
            logger.info("音频转换成功")
            
            return {
                'audio_path': output_wav,
                'title': title,
                'duration': duration,
                'url': url
            }
    except Exception as e:
        logger.error(f"下载视频音频失败: {e}")
        raise


# 创建 FastAPI 应用
app = FastAPI(
    title="FunASR 语音识别 API",
    description="支持音频和视频文件的语音转文字服务",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """根路径"""
    return {
        "service": "FunASR 语音识别 API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "device": _model_cache.get('device', 'not loaded'),
        "model_loaded": 'model' in _model_cache
    }


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """
    语音/视频转文字接口
    
    - **file**: 音频或视频文件
      - 支持音频格式: wav, mp3, m4a, flac, aac, ogg, wma
      - 支持视频格式: mp4, avi, mkv, mov, wmv, flv, webm
    
    返回:
    - **success**: 是否成功
    - **text**: 识别出的文本
    - **duration**: 音频时长（秒）
    - **processing_time**: 处理耗时（秒）
    """
    start_time = time.time()
    
    # 获取文件扩展名
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in AUDIO_EXTENSIONS and file_ext not in VIDEO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式: {file_ext}。支持的格式: {AUDIO_EXTENSIONS | VIDEO_EXTENSIONS}"
        )
    
    # 创建临时文件
    temp_dir = tempfile.mkdtemp()
    temp_input = os.path.join(temp_dir, f"input{file_ext}")
    temp_audio = os.path.join(temp_dir, "audio.wav")
    
    try:
        # 保存上传的文件
        content = await file.read()
        with open(temp_input, 'wb') as f:
            f.write(content)
        
        logger.info(f"处理文件: {file.filename} ({len(content) / 1024 / 1024:.2f} MB)")
        
        # 如果是视频，先提取音频
        if file_ext in VIDEO_EXTENSIONS:
            logger.info("正在从视频中提取音频...")
            if not extract_audio_from_video(temp_input, temp_audio):
                raise HTTPException(status_code=400, detail="无法从视频中提取音频")
            audio_path = temp_audio
        else:
            audio_path = temp_input
        
        # 加载音频
        audio_data, sample_rate, duration = load_audio(audio_path)
        logger.info(f"音频信息: 采样率={sample_rate}, 时长={duration:.2f}秒")
        
        # 获取模型并识别
        model = get_model()
        
        # SenseVoiceSmall 参数配置
        result = model.generate(
            input=audio_data,
            cache={},
            language="auto",      # 自动检测语言 (zh/en/ja/ko/yue)
            use_itn=True,         # 使用逆文本正则化（数字转换等）
            batch_size_s=60,
            merge_vad=True,       # 合并 VAD 切片
            merge_length_s=15,
        )
        
        # 提取文本（SenseVoiceSmall 需要富文本后处理）
        text = ""
        if result and len(result) > 0:
            try:
                from funasr.utils.postprocess_utils import rich_transcription_postprocess
                for item in result:
                    if 'text' in item:
                        # 使用富文本后处理提取纯文本
                        text += rich_transcription_postprocess(item['text'])
            except ImportError:
                # 如果没有后处理函数，直接使用原始文本
                for item in result:
                    if 'text' in item:
                        text += item['text']
        
        processing_time = time.time() - start_time
        
        logger.info(f"识别完成: {text[:50]}... (耗时: {processing_time:.2f}秒)")
        
        return JSONResponse(content={
            "success": True,
            "text": text,
            "duration": round(duration, 2),
            "processing_time": round(processing_time, 2),
            "model": _model_cache.get('model_name', 'unknown')
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"处理失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        import shutil
        try:
            shutil.rmtree(temp_dir)
        except:
            pass


from pydantic import BaseModel

class UrlRequest(BaseModel):
    url: str

@app.post("/transcribe_url")
async def transcribe_url(request: UrlRequest):
    """
    从视频链接转写文字
    
    - **url**: 视频链接 (支持 YouTube, Bilibili, 抖音等)
    
    返回:
    - **success**: 是否成功
    - **text**: 识别出的文本
    - **title**: 视频标题
    - **duration**: 时长（秒）
    - **processing_time**: 处理耗时（秒）
    """
    start_time = time.time()
    temp_dir = tempfile.mkdtemp()
    
    try:
        logger.info(f"开始处理 URL: {request.url}")
        
        # 下载音频
        logger.info("正在下载视频音频...")
        download_info = download_audio_from_url(request.url, temp_dir)
        audio_path = download_info['audio_path']
        video_title = download_info['title']
        
        logger.info(f"下载完成: {video_title}")
        
        # 加载音频
        audio_data, sample_rate, duration = load_audio(audio_path)
        logger.info(f"音频信息: 采样率={sample_rate}, 时长={duration:.2f}秒")
        
        # 获取模型并识别
        model = get_model()
        
        result = model.generate(
            input=audio_data,
            cache={},
            language="auto",
            use_itn=True,
            batch_size_s=60,
            merge_vad=True,
            merge_length_s=15,
        )
        
        # 提取文本
        text = ""
        if result and len(result) > 0:
            try:
                from funasr.utils.postprocess_utils import rich_transcription_postprocess
                for item in result:
                    if 'text' in item:
                        text += rich_transcription_postprocess(item['text'])
            except ImportError:
                for item in result:
                    if 'text' in item:
                        text += item['text']
        
        processing_time = time.time() - start_time
        
        logger.info(f"识别完成: {text[:50]}... (耗时: {processing_time:.2f}秒)")
        
        return JSONResponse(content={
            "success": True,
            "text": text,
            "title": video_title,
            "duration": round(duration, 2),
            "processing_time": round(processing_time, 2),
            "model": _model_cache.get('model_name', 'unknown')
        })
        
    except Exception as e:
        logger.error(f"处理 URL 失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        import shutil
        try:
            shutil.rmtree(temp_dir)
        except:
            pass


@app.on_event("startup")
async def startup_event():
    """服务启动时预加载模型"""
    logger.info("FunASR API 服务启动中...")
    # 可选：取消下面的注释以在启动时预加载模型
    # get_model()


if __name__ == "__main__":
    print("=" * 60)
    print("FunASR 语音识别 API 服务")
    print("=" * 60)
    print("API 文档: http://localhost:8000/docs")
    print("健康检查: http://localhost:8000/health")
    print("转写接口: POST http://localhost:8000/transcribe")
    print("=" * 60)
    
    uvicorn.run(
        "funasr_api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
