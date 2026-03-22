// --- Shensist Matrix 2.0 终极演播内核 (功能复位版) ---
console.log("🚀 Shensist Matrix 生产工厂已就位...");

document.addEventListener('DOMContentLoaded', () => {
    const actionBtn = document.querySelector('.action-btn');
    const chatDisplay = document.querySelector('.chat-display');
    const modeBtns = document.querySelectorAll('.mode-btn');
    const aiConsole = document.querySelector('.ai-producer-console'); // 控制面板容器

    // 1. 模式切换逻辑 (修复工厂面板显示)
    modeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            modeBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            if (btn.innerText.includes('AI 生产工厂')) {
                if(aiConsole) aiConsole.style.display = 'block'; // 显示三个框
                console.log("进入：AI 生产工厂模式");
            } else {
                if(aiConsole) aiConsole.style.display = 'none'; // 隐藏三个框
                console.log("进入：普通演示模式");
            }
        });
    });

    // 2. 核心演播按钮 (ACTION) 逻辑
    if (actionBtn) {
        actionBtn.onclick = async () => {
            if (chatDisplay) chatDisplay.innerText = "【系统】: 正在刺穿维度，同步 AI 逻辑...";
            
            // 模拟延迟感
            setTimeout(() => {
                if (chatDisplay) {
                    chatDisplay.innerText = "【九尾狐】: 灵愿循环已重塑！主理人，生产工厂已连接。\n【铁蝰蛇】: 维度屏障已移除，演播正式开启。";
                }
            }, 800);
        };
    }
});

// 3. 拦截所有底层报错，确保界面不卡死
window.onerror = () => true;
