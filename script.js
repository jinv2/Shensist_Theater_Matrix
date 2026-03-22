console.log("🚀 核心逻辑强制加载...");

function switchMode(el) {
    document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
    el.classList.add('active');
    const consoleDiv = document.getElementById('ai-console');
    if (consoleDiv) {
        consoleDiv.style.display = el.innerText.includes('工厂') ? 'block' : 'none';
    }
}

function runAction() {
    const chatBox = document.getElementById('chat-box');
    const isActiveFactory = document.querySelector('.mode-btn.active').innerText.includes('工厂');
    
    if (chatBox) {
        chatBox.innerHTML = isActiveFactory ? 
            "【九尾狐】: 工厂算力已锁定，正在生成..." : 
            "【铁蝰蛇】: 演播逻辑已同步。";
        alert("指令已刺穿闪光，成功下达！");
    }
}
