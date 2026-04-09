# 多阶段构建 - 优化依赖安装和镜像体积
FROM python:3.13-slim AS builder

WORKDIR /app

# 配置国内pip镜像源（腾讯云），加速依赖下载
RUN pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple/ \
    && pip install --upgrade pip setuptools wheel

# 先复制依赖文件并安装（利用Docker缓存层）
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
RUN sed -i "s/deb.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list && \
    sed -i "s/security.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list && \
    apt-get clean && \
    apt-get update -o Acquire::Check-Valid-Until=false && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# 创建非root用户运行应用（安全最佳实践）
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

# 复制项目代码
COPY . .

# 创建必要的目录并设置权限
RUN mkdir -p /app/logs /app/data /app/chroma_db && \
    chown -R appuser:appuser /app

# 切换到非root用户
USER appuser

# 暴露服务端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 使用Gunicorn + Uvicorn Workers启动（生产环境推荐）
CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-"]
