#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试 FunASR API 服务"""

import requests
import sys

API_URL = "http://localhost:8000"

def test_health():
    """测试健康检查"""
    print("测试健康检查...")
    resp = requests.get(f"{API_URL}/health")
    print(f"  状态码: {resp.status_code}")
    print(f"  响应: {resp.json()}")
    return resp.status_code == 200

def test_transcribe(file_path):
    """测试转写接口"""
    print(f"\n测试转写接口: {file_path}")
    
    with open(file_path, 'rb') as f:
        files = {'file': (file_path.split('\\')[-1], f)}
        resp = requests.post(f"{API_URL}/transcribe", files=files)
    
    print(f"  状态码: {resp.status_code}")
    result = resp.json()
    print(f"  成功: {result.get('success')}")
    print(f"  文本: {result.get('text')}")
    print(f"  时长: {result.get('duration')}秒")
    print(f"  处理时间: {result.get('processing_time')}秒")
    
    return resp.status_code == 200

if __name__ == "__main__":
    print("=" * 60)
    print("FunASR API 测试")
    print("=" * 60)
    
    # 测试健康检查
    if not test_health():
        print("健康检查失败！请确保服务已启动。")
        sys.exit(1)
    
    # 测试音频转写
    audio_file = r"d:\workspace\FunASR\runtime\funasr_api\asr_example.wav"
    test_transcribe(audio_file)
    
    print("\n" + "=" * 60)
    print("测试完成！")
