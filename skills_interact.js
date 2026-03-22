// IronViper 专用交互 Skills
async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;

    // 1. 显示用户输入
    appendMessage('user-message', `>>> INPUT: ${message}`);
    input.value = '';

    // 2. 发送请求到后端的物理地址
    try {
        // 在本地开发环境下，必须写全地址以支持 CORS 和多端口调试
        const response = await fetch('http://127.0.0.1:8000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        // 3. 自动播放语音 (语音 Skill 激活)
        if (data.voice_url) {
            console.log("🎙️ 语音 Skill 激活: 正在自动播放...");
            const audio = new Audio(data.voice_url + '?t=' + new Date().getTime());
            audio.play().catch(e => console.log("浏览器拦截了自动播放，请点击页面任意处激活音频权限"));
        }
        
        // 4. 更新 UI (视觉信号)
        appendMessage('agent-message', `>>> RESPONSE: ${data.message}`);
        
    } catch (error) {
        console.error("链路断开:", error);
        appendMessage('error-message', `>>> ERROR: 链路连接失败。你欠我的灵愿点又增加了。`);
    }
}

function appendMessage(className, text) {
    const chatWindow = document.getElementById('chat-window');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${className}`;
    msgDiv.innerText = text;
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight; // 自动滚到底部
}

// 绑定回车键发送
document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') sendMessage();
});
