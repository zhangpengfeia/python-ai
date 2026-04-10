# 多阶段构建 - 优化依赖安装和镜像体积

# 第一阶段：构建依赖
FROM python:3.13-slim AS builder

WORKDIR /app

# 配置国内pip镜像源（腾讯云），加速依赖下载
RUN pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple/ \
    && pip install --upgrade pip setuptools wheel

# 先安装 packaging（解决 langchain-core 的依赖问题）
RUN pip install --no-cache-dir --prefix=/install packaging

# 再安装其他依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# 第二阶段：运行时镜像
FROM python:3.13-slim

WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    ENVIRONMENT=production

# 从builder阶段复制已安装的依赖
COPY --from=builder /install /usr/local

# 安装curl用于健康检查（最小化安装）
# 替换阿里云源，解决国内 apt 卡住
RUN sed -i 's|http://deb.debian.org|https://mirrors.aliyun.com|g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's|http://security.debian.org|https://mirrors.aliyun.com|g' /etc/apt/sources.list.d/debian.sources && \
    apt-get clean && \
    apt-get update -o Acquire::Check-Valid-Until=false && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# 复制项目代码（在创建用户之前，避免权限问题）
COPY . .

# 创建必要的目录
RUN mkdir -p /app/logs /app/data /app/chroma_db

# 创建非root用户运行应用（安全最佳实践）
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser && \
    chown -R appuser:appuser /app

# 切换到非root用户
USER appuser

# 暴露服务端口
EXPOSE 8200

# 使用 Uvicorn 直接启动（与 main.py 保持一致）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8200", "--workers", "4"]
