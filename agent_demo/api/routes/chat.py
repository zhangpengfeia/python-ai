from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Dict, Any
from agent.react_agent import ReactAgent
from api.deps import get_agent
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


# 1. 定义消息结构
class Message(BaseModel):
    role: Literal["user", "assistant", "system"] = Field(..., description="消息角色")
    content: str = Field(..., description="消息内容")


# 2. 定义符合前端CustomInput要求的请求模型
class CustomChatRequest(BaseModel):
    messages: List[Message] = Field(..., description="消息列表，包含完整的对话历史")
    stream: Optional[bool] = Field(True, description="是否启用流式输出")
    model: Optional[str] = Field("qwen2.5-7b-instruct", description="模型名称")


# 3. 改造后的流式对话接口
@router.post("/stream")
async def chat_stream(
        request: CustomChatRequest,
        agent: ReactAgent = Depends(get_agent)
):
    try:
        # 参数校验
        if not request.messages:
            raise HTTPException(status_code=400, detail="消息列表不能为空")
        
        # 获取最后一条用户消息
        last_user_message = None
        for msg in reversed(request.messages):
            if msg.role == "user":
                last_user_message = msg.content
                break
        
        if not last_user_message or not last_user_message.strip():
            raise HTTPException(status_code=400, detail="用户查询内容不能为空")
        
        logger.info(f"收到请求 - 模型: {request.model}, 消息数: {len(request.messages)}")
        
        def event_generator():
            try:
                chunk_count = 0
                # 真正的流式：逐个接收并立即发送
                for chunk in agent.execute_stream(last_user_message):
                    chunk_count += 1
                    # 构造流式数据格式
                    stream_data = {
                        "content": chunk,
                        "isStreaming": True,
                        "progress": 0
                    }
                    yield f"data: {json.dumps(stream_data, ensure_ascii=False)}\n\n"
                
                # 发送结束标记
                yield "data: [DONE]\n\n"

            except Exception as e:
                logger.error(f"Agent执行错误: {str(e)}", exc_info=True)
                # 错误信息流式返回
                error_data = {
                    "content": f"⚠️ 系统错误: {str(e)}",
                    "isStreaming": False,
                    "progress": 0
                }
                yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"
                yield "data: [DONE]\n\n"

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
            }
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"接口初始化错误: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="服务器内部错误")


# 对话历史接口（保持不变）
@router.get("/history")
async def get_history(session_id: str = "default"):
    return {"history": []}
