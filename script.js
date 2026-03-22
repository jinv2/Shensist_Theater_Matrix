// --- Shensist Matrix 2.0 终极全能内核 ---
console.log("🚀 Shensist Matrix 双模系统已就绪...");

document.addEventListener('DOMContentLoaded', () => {
    const actionBtn = document.querySelector('.action-btn');
    const chatDisplay = document.querySelector('.chat-display');
    const modeBtns = document.querySelectorAll('.mode-btn');
    const aiConsole = document.querySelector('.ai-producer-console');
    
    let currentMode = '普通演示模式'; // 默认模式

    // 1. 模式切换：精准控制面板显隐与状态
    modeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            modeBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentMode = btn.innerText.trim();
            
            if (currentMode.includes('AI 生产工厂')) {
                if(aiConsole) aiConsole.style.display = 'block';
                console.log("切换至：工厂模式");
            } else {
                if(aiConsole) aiConsole.style.display = 'none';
                console.log("切换至：普通模式");
            }
        });
    });

    // 2. 演播核心 (ACTION)：根据模式执行不同灵魂
    if (actionBtn) {
        actionBtn.onclick = async () => {
            if (!chatDisplay) return;

            // 统一loading状态
            chatDisplay.innerHTML = '<span style="color: #ff0000;">⏳ 正在调集维度资源...</span>';

            setTimeout(() => {
                if (currentMode.includes('AI 生产工厂')) {
                    // 工厂模式逻辑
                    chatDisplay.innerHTML = "【九尾狐】: 生产工厂逻辑已接入。\n【铁蝰蛇】: 正在根据主理人 Prompt 实时重塑山海经位面...";
                } else {
                    // 普通模式逻辑 (修复点)
                    chatDisplay.innerHTML = "【九尾狐】: 灵愿循环正常运转。\n【系统】: 当前处于标准演播频率，全线逻辑同步完成。";
                    alert("普通演播指令已确认！");
                }
            }, 600);
        };
    }
});

// 3. 错误拦截
window.onerror = () => true;
