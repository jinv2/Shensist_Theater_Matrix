import openai
import json

def generate_script(topic, model="deepseek-chat", api_key=None):
    """
    核心 Skill：利用【动态指定】的大模型瞬间生成 10 轮高对抗性剧本
    """
    
    # 🎙️ 动态匹配 Base URL (根据模型名称特征)
    base_url = "https://api.deepseek.com/v1"
    if "gpt" in model or "openai" in model:
        base_url = "https://api.openai.com/v1"
    elif "claude" in model:
        base_url = "https://api.anthropic.com/v1" # 这里通常需要适配器，但保持 OpenAI 兼容性尝试
    elif "gemini" in model:
        base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    
    # 如果用户没填 KEY 且模型是 DeepSeek，可以尝试使用环境变量中的兜底 KEY (如果有的话)
    active_key = api_key or "YOUR_FALLBACK_KEY_IF_ANY"
    
    client = openai.OpenAI(api_key=active_key, base_url=base_url)

    prompt = f"""
    你现在是神思庭（Shensist）的首席剧作家。
    场景：一个数字电影院的大屏幕内。
    人物：
    1. 铁蝰蛇 (@mmmmmmmm1.ironviperh)：冷酷、暴戾、收债人、充满压迫感、说话简洁有力。
    2. 九尾狐 (@mmmmmmmm1.foxqueenah)：妩媚、狡黠、幻境主人、绵里藏针、喜欢戏谑。
    
    剧情主题：{topic}
    
    任务：编写10轮对峙台词（由铁蝰蛇发起，九尾狐回击，依次循环）。
    要求：
    - 不要包含角色名字前缀。
    - 语气要极度符合人设。
    - 铁蝰蛇想要解决问题或索赔，九尾狐负责周旋或挑衅。
    - 输出格式必须是严格的 JSON 数组，包含且仅包含以下结构：
    [
      {{"actor_id": "left", "text": "铁蝰蛇的第一句台词"}},
      {{"actor_id": "right", "text": "九尾狐的第一句回击"}},
      ...
    ]
    """
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一个专业的电影编剧。你只输出 JSON 数组，不包含任何 Markdown 代码块或其他文字。"},
                {"role": "user", "content": prompt}
            ],
            response_format={ 'type': 'json_object' } if "deepseek" in model or "gpt-4o" in model else None
        )
        
        raw_content = response.choices[0].message.content.strip()
        # 清洗可能存在的 Markdown 格式
        if raw_content.startswith("```json"):
            raw_content = raw_content[7:-3].strip()
        elif raw_content.startswith("```"):
            raw_content = raw_content[3:-3].strip()
            
        script_data = json.loads(raw_content)
        
        # 兼容不同的 JSON 返回结构
        if isinstance(script_data, dict):
            for key in ["script", "dialogue", "conversation", "lines"]:
                if key in script_data: return script_data[key]
        
        return script_data 
        
    except Exception as e:
        print(f"❌ AI 剧本生成失败 ({model}): {e}")
        return [
            {"actor_id": "left", "text": f"（AI 提示：{model} 连接失败，请检查 API KEY）关于 {topic}，你得给我个说法！"},
            {"actor_id": "right", "text": "哎呀，这会儿大脑断线了，咱们还是按老规矩办吧~"}
        ] * 5
