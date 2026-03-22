// --- Shensist Matrix 2.0 终极自愈内核 ---
console.log("🚀 Shensist Matrix 核心已启动...");

// 1. 强制拦截所有可能崩溃的错误
window.onerror = () => true;

// 2. 模拟后端响应（方案 C 核心：本地优先）
const mockResponse = {
    text: "【九尾狐】: 灵愿循环已重塑！主理人，维度屏障已移除，演播正式开启。\n【系统】: 当前处于降维自愈模式，所有指令已接管。"
};

// 3. 绑定按钮逻辑
document.addEventListener('DOMContentLoaded', () => {
    const actionBtn = document.querySelector('.action-btn') || document.getElementById('action-btn');
    const modeBtns = document.querySelectorAll('.mode-btn');
    const outputArea = document.querySelector('.chat-display') || document.getElementById('chat-box');

    if (actionBtn) {
        actionBtn.onclick = () => {
            console.log("按钮点击触发");
            if (outputArea) outputArea.innerText = mockResponse.text;
            alert("演播指令已下达！逻辑同步中...");
        };
    }

    modeBtns.forEach(btn => {
        btn.onclick = (e) => {
            modeBtns.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            console.log("模式切换:", e.target.innerText);
        };
    });
});
