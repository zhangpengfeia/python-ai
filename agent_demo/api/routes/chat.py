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


# 1. 定义符合前端要求的请求模型
class CustomChatRequest(BaseModel):
    query: str = Field(..., description="用户输入的查询内容")
    role: Literal["user"] = Field("user", description="消息角色，固定为user")
    stream: bool = Field(True, description="是否启用流式输出，建议保持True")
    model: str = Field(..., description="模型名称，例如 qwen2.5-7b-instruct")
    session_id: Optional[str] = Field("default", description="会话ID，支持多会话")


# 2. 改造后的流式对话接口
@router.post("/stream")
async def chat_stream(
        request: CustomChatRequest,
        agent: ReactAgent = Depends(get_agent)
):
    try:
        # 参数校验
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="查询内容不能为空")
        logger.info(f"收到请求 - 模型: {request.model}, 会话ID: {request.session_id}")

        async def event_generator():
            try:
                # 收集所有chunk以计算进度（实际生产中可根据token数或迭代进度动态计算）
                chunks = []
                for chunk in agent.execute_stream(request.query):
                    chunks.append(chunk)
                total_chunks = len(chunks)
                # 发送流式内容块（带进度）
                for idx, chunk in enumerate(chunks):
                    # 计算进度（避免除以0）
                    progress = int((idx + 1) / total_chunks * 100) if total_chunks > 0 else 100

                    # 构造流式数据格式
                    stream_data = {
                        "content": chunk,
                        "isStreaming": True,
                        "progress": progress
                    }
                    yield f"data: {json.dumps(stream_data, ensure_ascii=False)}\n\n"

                # 发送最终完成块（带附件）
                final_data = {
                    "content": "",
                    "attachments": [
                        {
                            "name": "科技新闻总结.pdf",
                            "url": "https://x.ant.design/download/report.pdf",
                            "type": "pdf",
                            "size": 102400
                        }
                    ],
                    "isComplete": True
                }
                yield f"data: {json.dumps(final_data, ensure_ascii=False)}\n\n"

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