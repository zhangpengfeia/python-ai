from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Dict, Any
from agent.react_agent import ReactAgent
from api.deps import get_agent
from rag.chat_session import ChatSession
import json
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


# ==================== 数据模型定义 ====================

# 1. 定义消息结构
class Message(BaseModel):
    role: Literal["user", "assistant", "system"] = Field(..., description="消息角色")
    content: str = Field(..., description="消息内容")


# 2. 定义符合前端CustomInput要求的请求模型
class CustomChatRequest(BaseModel):
    messages: List[Message] = Field(..., description="消息列表，包含完整的对话历史")
    stream: Optional[bool] = Field(True, description="是否启用流式输出")
    model: Optional[str] = Field("qwen2.5-7b-instruct", description="模型名称")
    session_id: Optional[str] = Field(None, description="会话ID，不提供则自动创建新会话")


# 3. 创建会话请求
class CreateSessionRequest(BaseModel):
    session_name: Optional[str] = Field("新对话", description="会话名称")


# 4. 重命名会话请求
class RenameSessionRequest(BaseModel):
    session_name: str = Field(..., description="新的会话名称")


# 5. 添加消息请求
class AddMessageRequest(BaseModel):
    session_id: str = Field(..., description="会话ID")
    role: Literal["user", "assistant"] = Field(..., description="消息角色")
    content: str = Field(..., description="消息内容")
    use_rag: Optional[int] = Field(0, description="是否使用RAG，0或1")
    md5: Optional[str] = Field(None, description="消息MD5值")


# ==================== 依赖注入 ====================

def get_chat_session():
    """获取聊天会话管理器实例"""
    return ChatSession()


# ==================== 会话管理接口 ====================

@router.post("/session/create", summary="创建新会话")
def create_session(request: CreateSessionRequest, session_manager: ChatSession = Depends(get_chat_session)):
    """
    创建一个新的聊天会话

    - **session_name**: 会话名称（可选，默认"新对话"）

    返回：
    - **session_id**: 新生成的会话ID
    - **session_name**: 会话名称
    - **create_time**: 创建时间
    """
    try:
        session_id = session_manager.create_session(request.session_name)
        if not session_id:
            raise HTTPException(status_code=500, detail="创建会话失败")

        return {
            "code": 200,
            "message": "创建成功",
            "data": {
                "session_id": session_id,
                "session_name": request.session_name,
                "create_time": datetime.now().isoformat()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建会话异常: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"创建会话失败: {str(e)}")


@router.get("/session/list", summary="获取会话列表")
def list_sessions(
        limit: int = 20,
        session_manager: ChatSession = Depends(get_chat_session)
):
    """
    获取会话列表（按更新时间倒序）

    - **limit**: 返回数量限制（默认20）

    返回：
    - **sessions**: 会话列表
    """
    try:
        sessions = session_manager.list_sessions(limit)
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "sessions": sessions,
                "total": len(sessions)
            }
        }
    except Exception as e:
        logger.error(f"获取会话列表异常: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取会话列表失败: {str(e)}")


@router.put("/session/{session_id}/rename", summary="重命名会话")
def rename_session(
        session_id: str,
        request: RenameSessionRequest,
        session_manager: ChatSession = Depends(get_chat_session)
):
    """
    重命名指定会话

    - **session_id**: 会话ID（路径参数）
    - **session_name**: 新的会话名称

    返回：
    - **success**: 是否成功
    """
    try:
        success = session_manager.rename_session(session_id, request.session_name)
        if not success:
            raise HTTPException(status_code=500, detail="重命名失败")

        return {
            "code": 200,
            "message": "重命名成功",
            "data": {
                "session_id": session_id,
                "session_name": request.session_name
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"重命名会话异常: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"重命名失败: {str(e)}")


@router.delete("/session/{session_id}", summary="删除会话")
def delete_session(
        session_id: str,
        session_manager: ChatSession = Depends(get_chat_session)
):
    """
    删除指定会话及其所有消息

    - **session_id**: 会话ID（路径参数）

    返回：
    - **success**: 是否成功
    """
    try:
        # 先清空消息，再删除会话（如果需要删除会话记录，需要在 ChatSession 中添加方法）
        session_manager.clear_history(session_id)
        return {
            "code": 200,
            "message": "删除成功",
            "data": {
                "session_id": session_id
            }
        }
    except Exception as e:
        logger.error(f"删除会话异常: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")


# ==================== 消息管理接口 ====================

@router.post("/message/add", summary="添加消息")
def add_message(
        request: AddMessageRequest,
        session_manager: ChatSession = Depends(get_chat_session)
):
    """
    保存一条聊天记录到数据库
    - **session_id**: 会话ID
    - **role**: 消息角色（user/assistant）
    - **content**: 消息内容
    - **use_rag**: 是否使用RAG（0或1）
    - **md5**: 消息MD5值（可选）

    返回：
    - **success**: 是否成功
    """
    try:
        success = session_manager.add_message(
            session_id=request.session_id,
            role=request.role,
            content=request.content,
            use_rag=request.use_rag,
            md5=request.md5
        )
        if not success:
            raise HTTPException(status_code=500, detail="保存消息失败")

        return {
            "code": 200,
            "message": "保存成功",
            "data": {
                "session_id": request.session_id,
                "role": request.role
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"保存消息异常: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"保存消息失败: {str(e)}")


@router.get("/message/history/{session_id}", summary="获取会话历史消息")
def get_message_history(
        session_id: str,
        limit: int = 50,
        session_manager: ChatSession = Depends(get_chat_session)
):
    """
    获取指定会话的历史消息

    - **session_id**: 会话ID（路径参数）
    - **limit**: 返回消息数量限制（默认50）

    返回：
    - **messages**: 消息列表（按时间正序）
    """
    try:
        messages = session_manager.get_history(session_id, limit)
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "session_id": session_id,
                "messages": messages,
                "total": len(messages)
            }
        }
    except Exception as e:
        logger.error(f"获取历史消息异常: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取历史消息失败: {str(e)}")


@router.delete("/message/history/{session_id}", summary="清空会话消息")
def clear_message_history(
        session_id: str,
        session_manager: ChatSession = Depends(get_chat_session)
):
    """
    清空指定会话的所有消息（不删除会话本身）
    - **session_id**: 会话ID（路径参数）
    返回：
    - **success**: 是否成功
    """
    try:
        success = session_manager.clear_history(session_id)
        if not success:
            raise HTTPException(status_code=500, detail="清空失败")

        return {
            "code": 200,
            "message": "清空成功",
            "data": {
                "session_id": session_id
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"清空历史消息异常: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"清空失败: {str(e)}")


# ==================== 聊天接口 ====================

@router.post("/stream", summary="流式对话接口")
async def chat_stream(
        request: CustomChatRequest,
        agent: ReactAgent = Depends(get_agent),
        session_manager: ChatSession = Depends(get_chat_session)
):
    """
    流式对话接口，支持会话管理和历史记录
    - **messages**: 消息列表（包含完整对话历史）
    - **session_id**: 会话ID（可选，不提供则自动创建）
    - **stream**: 是否启用流式输出（默认True）
    - **model**: 模型名称
    返回：SSE 流式响应
    """
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

        # 处理会话ID
        session_id = request.session_id
        if not session_id:
            # 自动创建新会话
            session_id = session_manager.create_session("新对话")
            logger.info(f"自动创建新会话: {session_id}")

        logger.info(f"收到请求 - 会话ID: {session_id}, 消息数: {len(request.messages)}")

        # 保存用户消息到数据库
        session_manager.add_message(
            session_id=session_id,
            role="user",
            content=last_user_message,
            use_rag=0
        )

        def event_generator():
            try:
                full_response = []
                chunk_count = 0
                # 真正的流式：逐个接收并立即发送
                for chunk in agent.execute_stream(last_user_message):
                    chunk_count += 1
                    full_response.append(chunk)

                    # 构造流式数据格式
                    stream_data = {
                        "content": chunk,
                        "isStreaming": True,
                        "progress": 0,
                        "session_id": session_id
                    }
                    yield f"data: {json.dumps(stream_data, ensure_ascii=False)}\n\n"

                # 保存助手回复到数据库
                assistant_response = "".join(full_response)
                session_manager.add_message(
                    session_id=session_id,
                    role="assistant",
                    content=assistant_response,
                    use_rag=0
                )

                # 发送结束标记
                yield f"data: {json.dumps({'content': '', 'isComplete': True, 'session_id': session_id}, ensure_ascii=False)}\n\n"
                yield "data: [DONE]\n\n"

            except Exception as e:
                logger.error(f"Agent执行错误: {str(e)}", exc_info=True)
                # 错误信息流式返回
                error_data = {
                    "content": f"⚠️ 系统错误: {str(e)}",
                    "isStreaming": False,
                    "progress": 0,
                    "session_id": session_id
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



@router.get("/history", summary="获取会话历史（兼容旧接口）")
def get_history(
        session_id: str = "default",
        limit: int = 50,
        session_manager: ChatSession = Depends(get_chat_session)
):
    """
    兼容旧版本的 history 接口

    - **session_id**: 会话ID
    - **limit**: 消息数量限制
    """
    try:
        messages = session_manager.get_history(session_id, limit)
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "session_id": session_id,
                "history": messages,
                "total": len(messages)
            }
        }
    except Exception as e:
        logger.error(f"获取历史异常: {str(e)}", exc_info=True)
        return {
            "code": 500,
            "message": f"获取失败: {str(e)}",
            "data": {
                "session_id": session_id,
                "history": [],
                "total": 0
            }
        }
