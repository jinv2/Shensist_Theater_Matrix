import asyncio
import edge_tts
import os

# 定义神思庭宇宙的角色音色矩阵
# 你可以根据需要随时在这里增加新主角
VOICE_MAP = {
    "@mmmmmmmm1.verdantnam": "zh-CN-XiaoxiaoNeural",     # 小青：温柔女声
    "@mmmmmmmm1.ironviperh": "zh-CN-YunxiNeural",       # 恶霸：冷酷男声
    "@mmmmmmmm1.foxqueenah": "zh-CN-XiaoyiNeural",      # 九尾狐：妩媚女声
    "@mmmmmmmm1r": "zh-CN-YunyangNeural",               # 男主：正气男声
    "default": "zh-CN-YunxiNeural"
}

async def generate_voice(text, character_id, output_path="./ui_frontend/assets/speech.mp3"):
    """
    核心技能：将文字转为 MP3 语音
    """
    # 1. 自动匹配音色
    voice = VOICE_MAP.get(character_id, VOICE_MAP["default"])
    
    # 2. 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 3. 调用 Edge-TTS 引擎
    print(f"🎙️ [Shensist-Voice] 正在为 {character_id} 朗读: {text[:15]}...")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    return output_path

def speak(text, character_id, output_path="./ui_frontend/assets/speech.mp3"):
    """
    同步调用接口，方便在 Flask/App.py 中直接使用
    """
    try:
        asyncio.run(generate_voice(text, character_id, output_path))
        return True
    except Exception as e:
        print(f"❌ 语音生成失败: {e}")
        return False

if __name__ == "__main__":
    # 独立测试逻辑
    speak("这片领地的一草一木都标了价，明白了吗？", "@mmmmmmmm1.ironviperh")
