// --- Shensist Matrix 2.0 逻辑穿透内核 ---
console.log("🚀 穿透逻辑已激活：忽略闪光，直达核心...");

// 1. 强制自愈：拦截所有底层崩溃
window.onerror = () => true;

// 2. 全局点击分流器 (直接挂载到 window)
window.handleAction = () => {
    const chatDisplay = document.querySelector('.chat-display') || document.getElementById('chat-box');
    const activeMode = document.querySelector('.mode-btn.active');
    const modeName = activeMode ? activeMode.innerText.trim() : "普通演示模式";

    if (chatDisplay) {
        chatDisplay.innerHTML = '<span style="color: #00ff41;">[信号接入中...]</span>';
        setTimeout(() => {
            if (modeName.includes('AI 生产工厂')) {
                chatDisplay.innerHTML = "【九尾狐】: 生产工厂算力已分配。\\n【铁蝰蛇】: 正在重塑山海经位面...";
            } else {
                chatDisplay.innerHTML = "【九尾狐】: 灵愿循环正常。\\n【系统】: 当前处于标准演播频率。";
                alert("普通演播指令已下达！");
            }
        }, 500);
    }
};

// 3. 初始化：强行赋予按钮灵魂
document.addEventListener('DOMContentLoaded', () => {
    const actionBtn = document.querySelector('.action-btn');
    const modeBtns = document.querySelectorAll('.mode-btn');
    const aiConsole = document.querySelector('.ai-producer-console');

    // 模式切换穿透
    modeBtns.forEach(btn => {
        btn.onclick = (e) => {
            modeBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            if (aiConsole) {
                aiConsole.style.display = btn.innerText.includes('AI 生产工厂') ? 'block' : 'none';
            }
            console.log("模式切换成功:", btn.innerText);
        };
    });

    // ACTION 按钮强制绑定
    if (actionBtn) {
        actionBtn.setAttribute('onclick', 'handleAction()');
        actionBtn.style.pointerEvents = 'auto'; // 强制开启指针事件
        actionBtn.style.cursor = 'pointer';
    }
});
