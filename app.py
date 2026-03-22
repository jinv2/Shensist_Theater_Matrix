import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys

# --- 架构师注入：确保核心逻辑可访问 ---
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CORE_LOGIC_PATH = os.path.join(BASE_PATH, "core_logic")
sys.path.append(CORE_LOGIC_PATH)

import voice
import brain
from brain import generate_script

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 自动指向当前目录的 ui_frontend
UI_DIR = os.path.join(BASE_PATH, "ui_frontend")

@app.route('/')
def index():
    return send_from_directory(UI_DIR, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(UI_DIR, path)

import base64
import asyncio
import edge_tts

# --- 灵魂注入：内存级语音矩阵 ---
async def get_voice_base64(text, role_id):
    """瞬间将文字转为 Base64 音频，不留痕迹"""
    # 自动匹配音色矩阵 (适配 actor_id 或 role_id)
    v_name = "zh-CN-YunxiNeural" if ("viper" in role_id or "left" in role_id) else "zh-CN-XiaoyiNeural"
    try:
        communicate = edge_tts.Communicate(text, v_name)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        return base64.b64encode(audio_data).decode('utf-8')
    except Exception as e:
        print(f"❌ [Voice-Error] {role_id} 合成失败: {e}")
        return None

async def process_script_voices(script_data):
    """并行处理所有台词的语音合成"""
    tasks = [get_voice_base64(item['text'], item['actor_id']) for item in script_data]
    return await asyncio.gather(*tasks)

@app.route('/theater', methods=['POST'])
def theater_logic():
    data = request.json
    topic = data.get('topic', '纠纷')
    mode = data.get('mode', 'normal') # 🎬 获取模式：normal 或 ai_factory
    
    # 1. 🧠 剧本来源选择
    if mode == 'ai_factory':
        print(f"🔥 [Brain] 正在连接 AI 生产工厂 | 模型: {data.get('model')} | 主题: {topic}")
        # ⚡ 动态调用大脑，传入用户配置
        raw_script = generate_script(
            topic=topic,
            model=data.get('model', 'deepseek-chat'),
            api_key=data.get('api_key'),
            api_base=data.get('api_base')
        )
        script_data = raw_script.get('script', raw_script) if isinstance(raw_script, dict) else raw_script
    else:
        print(f"🔘 [Normal] 使用普通演示模式，生成主题: {topic}")
        # 普通模式：本地预设台词 (快速演示/兜底)
        script_data = [
            {"actor_id": "left", "text": f"普通模式：姓狐的，关于{topic}，我这关过不去！"},
            {"actor_id": "right", "text": "哎呀~ 这种小事，不值得动这么大火气。"},
            {"actor_id": "left", "text": f"少来这套！今天不给个交代，这幻境你就别想要了。"},
            {"actor_id": "right", "text": "那得看您有没有这个本事了，蝰蛇大人。"}
        ]

    final_script = []

    # 🎙️ 2. 内存级全同步并行语音生成 (Base64)
    print(f"🎙️ [Memory-Voice] 正在并行合成 {len(script_data)} 句台词...")
    try:
        # 使用 asyncio.run 自动处理循环生命周期 (更安全稳定)
        b64_results = asyncio.run(process_script_voices(script_data))
        
        for i, b64_audio in enumerate(b64_results):
            item = script_data[i]
            final_script.append({
                "actor_id": item['actor_id'],
                "text": item['text'],
                "audio_data": f"data:audio/mp3;base64,{b64_audio}" if b64_audio else ""
            })
    except Exception as e:
        print(f"❌ [Backend-Error] 语音处理阶段崩溃: {e}")
        # 即使语音完全失败，也至少返回文字剧本
        for item in script_data:
            final_script.append({
                "actor_id": item['actor_id'],
                "text": item['text'],
                "audio_data": ""
            })
    
    return jsonify(final_script)

if __name__ == '__main__':
    # 必须监听 0.0.0.0 和 7860 端口
    app.run(host='0.0.0.0', port=7860, debug=False)
