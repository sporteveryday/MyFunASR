import os
import json
import logging
import httpx
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Mistral AI Settings
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY", "") # 自己的apikey

async def analyze_text_with_llm(text: str) -> Optional[Dict[str, Any]]:
    """使用 Mistral Large 2 模型分析文本内容"""
    if not MISTRAL_API_KEY:
        logger.warning("MISTRAL_API_KEY 未设置，跳过 AI 分析")
        return None

    if not text or len(text.strip()) < 10:
        return {
            "summary": "内容过短，无法生成有效分析。",
            "highlights": [],
            "suggestions": []
        }

    prompt = f"""
    你是一个专业的会议/视频内容分析助手。请对以下识别出的文本进行深度分析：
    
    文本内容：
    "{text}"
    
    请按以下 JSON 格式返回结果：
    {{
        "summary": "一句精炼的话总结内容主旨",
        "highlights": ["重点要点1", "重点要点2", "重点要点3"],
        "suggestions": ["基于内容的行动建议1", "基于内容的建议2"]
    }}
    只需输出 JSON，不要有其他解释。
    """

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-large-latest",
        "messages": [
            {
                "role": "system",
                "content": "你是一个高效、精准的内容分析助手，仅以 JSON 格式回复。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "response_format": { "type": "json_object" },
        "temperature": 0.5
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(MISTRAL_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            content = result['choices'][0]['message']['content']
            return json.loads(content)
    except Exception as e:
        logger.error(f"Mistral API 调用失败: {str(e)}")
        return None
