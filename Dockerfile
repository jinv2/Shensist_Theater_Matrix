# 1. 使用官方镜像，它自带了 Python 和 Pip
FROM python:3.9-slim

# 2. 仅安装音频必须的 FFmpeg，不再安装冗余的 python3-pip
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# 3. 设置权限与用户
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:\$PATH"
WORKDIR /app

# 4. 使用绝对路径调用 Python 模块，彻底解决 "not found"
COPY --chown=user requirements.txt .
RUN /usr/local/bin/python -m pip install --no-cache-dir --upgrade pip && \
    /usr/local/bin/python -m pip install --no-cache-dir --upgrade -r requirements.txt

# 5. 拷贝全量逻辑
COPY --chown=user . .

# 6. 启动演播室
CMD ["/usr/local/bin/python", "app.py"]
