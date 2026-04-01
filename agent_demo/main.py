# main.py 最终完整代码
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import chat, rag, tools
from api.handlers import add_exception_handlers
import uvicorn

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

# ❌ 删除整个 if __name__ == "__main__" 块