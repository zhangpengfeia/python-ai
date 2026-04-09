# main.py 最终完整代码
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import chat, rag, tools
from api.handlers import add_exception_handlers
import uvicorn
import os

app = FastAPI(title="AI Agent API", version="1.0")

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(chat.router, prefix="/api/v1/chat", tags=["对话"])
app.include_router(rag.router, prefix="/api/v1/rag", tags=["RAG"])
app.include_router(tools.router, prefix="/api/v1/tools", tags=["工具"])

# 注册全局异常处理器
add_exception_handlers(app)

# 健康检查
@app.get("/health", tags=["基础"])
async def health_check():
    return {"status": "ok", "message": "AI服务正常运行"}

# 启动服务入口（必须添加）
if __name__ == "__main__":
    # 从环境变量读取配置，支持 Docker 部署
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8200))
    workers = int(os.getenv("WORKERS", 1))
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    # 生产环境使用 gunicorn，开发环境使用 uvicorn
    if workers > 1:
        import multiprocessing
        workers = min(workers, multiprocessing.cpu_count() * 2 + 1)
        print(f"启动 Gunicorn + Uvicorn Workers: {workers} 个worker进程")
        os.system(f"gunicorn main:app -k uvicorn.workers.UvicornWorker -b {host}:{port} --workers {workers} --timeout 120")
    else:
        print(f"启动 Uvicorn 开发服务器: {host}:{port}")
        uvicorn.run(
            app="main:app",
            host=host,
            port=port,
            reload=reload
        )
