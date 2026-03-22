let currentMode = 'normal'; // 🎬 默认为普通模式

// ⚡ 核心修正：统一 API 地址到本地 7860 端口 (Hugging Face 默认)
const API_URL = "http://127.0.0.1:7860/theater"; 

function setMode(mode) {
    currentMode = mode;
    const params = document.getElementById('director-params');
    
    // 💡 物理切换与动画控制
    if (mode === 'ai_factory') {
        params.style.display = 'flex';
        setTimeout(() => params.classList.add('active'), 10);
    } else {
        params.classList.remove('active');
        setTimeout(() => params.style.display = 'none', 500);
    }
    
    // UI 高亮切换
    document.getElementById('btn-normal').classList.toggle('active', mode === 'normal');
    document.getElementById('btn-factory').classList.toggle('active', mode === 'ai_factory');
    
    document.getElementById('subtitle').innerText = 
        mode === 'normal' ? "已进入：普通演示模式 (快速视觉校准)" : "已激活：AI 生产工厂 (准备深度对线)";
}

async function runTheater() {
    const topic = document.getElementById('input-topic').value;
    const model = document.getElementById('model-select').value;
    const apiKey = document.getElementById('user-api-key').value;
    const btn = document.getElementById('action-btn');
    const subtitle = document.getElementById('subtitle');

    if (currentMode === 'ai_factory' && !apiKey) {
        alert("⚠️ 架构师，请先填入 API KEY 以激活 AI 生产工厂！");
        return;
    }

    btn.disabled = true;
    subtitle.innerHTML = `<span style="color: #ff0000; font-weight: bold;">🎬 演员正在后台${currentMode === 'ai_factory' ? '对词(AI)' : '准备'}，请稍候...</span>`;

    try {
        const res = await fetch(API_URL, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ topic, mode: currentMode, model, api_key: apiKey })
        });
        if (!res.ok) throw new Error('网络断电');
        const data = await res.json();
        
        // 🚀 灵魂演播开始！
        await playPerformance(data);
        
    } catch (err) {
        console.error("剧场故障:", err);
        document.getElementById('subtitle').innerHTML = '<span style="color:red">❌ 剧场意外断电，请检查后台。</span>';
    } finally {
        btn.disabled = false;
    }
}

async function playPerformance(lines) {
    const subtitle = document.getElementById('subtitle');
    subtitle.innerText = "🚀 灵魂演播开始！";

    for (let line of lines) {
        // 1. ⚡ 物理视觉切换
        document.querySelectorAll('.actor').forEach(a => a.classList.remove('active'));
        const activeActor = document.getElementById(line.actor_id);
        if (activeActor) activeActor.classList.add('active');

        // 2. ⚡ 播放内存音频
        await new Promise((resolve) => {
            let audio = new Audio(line.audio_data);
            audio.oncanplaythrough = () => {
                subtitle.style.color = line.actor_id === 'left' ? '#ff4444' : '#ff44ff';
                subtitle.innerText = line.text;
                audio.play().catch(resolve);
            };
            audio.onended = () => setTimeout(resolve, 500);
            audio.onerror = resolve;
        });
    }
    subtitle.style.color = "#fff";
    subtitle.innerText = "🎬 演播结束。";
    document.querySelectorAll('.actor').forEach(a => a.classList.remove('active'));
}
