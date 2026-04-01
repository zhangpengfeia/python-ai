from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agent.react_agent import ReactAgent
from api.deps import get_agent
import json

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"  # 会话ID，支持多会话


# 流式对话接口（核心！）
@router.post("/stream")
async def chat_stream(request: ChatRequest, agent: ReactAgent = Depends(get_agent)):
    async def event_generator():
        # 调用你的Agent流式方法
        for chunk in agent.execute_stream(request.message):
            # 按SSE格式返回
            yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


# 对话历史（可选，用Redis/数据库存储）
@router.get("/history")
async def get_history(session_id: str = "default"):
    # 从存储中获取历史，这里简化返回
    return {"history": []}