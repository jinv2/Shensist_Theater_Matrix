import os
import sys
from huggingface_hub import HfApi

# 1. 强制声明系统默认编码
import importlib
importlib.reload(sys)

# 物理参数配置
TOKEN = "你的_HF_TOKEN"  # ⚡架构师，请在此填入真实的 Token
REPO_ID = "jinv2-shensist-theater-matrix" # 修正为正确的 Space ID

api = HfApi()

try:
    print(f"🚀 架构师，正在执行【字节流强穿】同步至: {REPO_ID}...")
    
    # 2. 将本地路径强制转为绝对路径
    # 注意：在 Linux 环境下，如果环境编码不是 UTF-8，可能会触发编码异常
    local_dir = os.path.abspath(".")
    
    api.upload_folder(
        folder_path=local_dir,
        repo_id=REPO_ID,
        repo_type="space",
        token=TOKEN,
        ignore_patterns=["venv/*", ".git/*", "__pycache__/*", "*.pyc"]
    )
    print("✅ [神思矩阵] 物理逻辑同步成功。")
except Exception as e:
    # 捕获原始错误，防止报错本身再次触发编码异常
    print(f"❌ 同步失败。")
    print(repr(e))
