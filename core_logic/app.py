import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import voice

app = Flask(__name__)
CORS(app)
# --- 架构师路径修正 ---
# 获取当前文件 (app.py) 所在的绝对路径
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
# 自动指向上一级目录的 ui_frontend
UI_DIR = os.path.join(os.path.dirname(BASE_PATH), "ui_frontend")

@app.route('/')
def index():
    return send_from_directory(UI_DIR, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(UI_DIR, path)
# ---------------------

import base64
import asyncio
import edge_tts

from brain import generate_script

# --- 灵魂注入：内存级语音矩阵 ---
async def get_voice_base64(text, role_id):
    """瞬间将文字转为 Base64 音频，不留痕迹"""
    # 自动匹配音色矩阵 (适配 actor_id 或 role_id)
    v_name = "zh-CN-YunxiNeural" if ("viper" in role_id or "left" in role_id) else "zh-CN-XiaoyiNeural"
    communicate = edge_tts.Communicate(text, v_name)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return base64.b64encode(audio_data).decode('utf-8')

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
            api_key=data.get('api_key')
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

    # 🎙️ 2. 内存级全同步语音生成 (Base64)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        for i, item in enumerate(script_data):
            role_id = item['actor_id']
            print(f"🎙️ [Memory-Voice] 正在为 {item['actor_id']} 合成: {item['text'][:15]}...")
            
            b64_audio = loop.run_until_complete(get_voice_base64(item['text'], role_id))
            final_script.append({
                "actor_id": item['actor_id'],
                "text": item['text'],
                "audio_data": f"data:audio/mp3;base64,{b64_audio}"
            })
    finally:
        loop.close()
    
    return jsonify(final_script)

if __name__ == '__main__':
    # 🚀 Hugging Face 必须监听 7860 端口
    app.run(host='0.0.0.0', port=7860, debug=True)
