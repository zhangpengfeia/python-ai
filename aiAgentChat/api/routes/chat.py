from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Union
from agent.react_agent import ReactAgent
from api.deps import get_agent
from rag.chat_controller import ChatSession
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter()

# ==================== 数据模型定义 ====================

class TextContent(BaseModel):
    """文本内容"""
    type: Literal["text"] = "text"
    text: str = Field(..., description="文本内容")

class ImageContent(BaseModel):
    """图片内容"""
    type: Literal["image"] = "image"
    image_url: str = Field(..., description="图片URL地址")
    description: Optional[str] = Field(None, description="图片描述")

ContentItem = Union[TextContent, ImageContent]

class Message(BaseModel):
    """消息结构，支持文本和图片混合内容"""
    role: Literal["user", "assistant", "system"] = Field(..., description="消息角色")
    content: Union[str, List[ContentItem]] = Field(..., description="消息内容，可以是纯文本或图文混合")

class CustomChatRequest(BaseModel):
    messages: List[Message] = Field(..., description="消息列表，包含完整的对话历史")
    stream: Optional[bool] = Field(True, description="是否启用流式输出")
    model: Optional[str] = Field("qwen2.5-7b-instruct", description="模型名称")
    session_id: Optional[str] = Field(None, description="会话ID，不提供则自动创建新会话")

class CreateSessionRequest(BaseModel):
    session_name: Optional[str] = Field("新对话", description="会话名称")

class RenameSessionRequest(BaseModel):
    session_name: str = Field(..., description="新的会话名称")

class AddMessageRequest(BaseModel):
    session_id: str = Field(..., description="会话ID")
    role: Literal["user", "assistant"] = Field(..., description="消息角色")
    content: Union[str, List[ContentItem]] = Field(..., description="消息内容")
    use_rag: Optional[int] = Field(0, description="是否使用RAG，0或1")
    md5: Optional[str] = Field(None, description="消息MD5值")

def get_chat_session():
    """获取聊天会话管理器实例"""
    return ChatSession()

# ==================== 会话管理接口 ====================

@router.post("/session/create", summary="创建新会话")
def create_session(request: CreateSessionRequest, session_manager: ChatSession = Depends(get_chat_session)):
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
    try:
        if session_id == "default-0":
            raise HTTPException(status_code=403, detail="默认会话不可重命名")
        
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
    try:
        if session_id == "default-0":
            raise HTTPException(status_code=403, detail="默认会话不可删除")
        
        success = session_manager.delete_session(session_id)
        if not success:
            raise HTTPException(status_code=500, detail="删除会话失败")
        
        return {
            "code": 200,
            "message": "删除成功",
            "data": {
                "session_id": session_id
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除会话异常: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")

# ==================== 消息管理接口 ====================

@router.post("/message/add", summary="添加消息")
def add_message(
        request: AddMessageRequest,
        session_manager: ChatSession = Depends(get_chat_session)
):
    try:
        content_str = _serialize_content(request.content)
        success = session_manager.add_message(
            session_id=request.session_id,
            role=request.role,
            content=content_str,
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
    try:
        messages = session_manager.get_history(session_id, limit)
        parsed_messages = [_parse_message_content(msg) for msg in messages]
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "session_id": session_id,
                "messages": parsed_messages,
                "total": len(parsed_messages)
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
@router.post("/stream", summary="流式对话接口（支持图片）")
async def chat_stream(
        request: CustomChatRequest,
        agent: ReactAgent = Depends(get_agent),
        session_manager: ChatSession = Depends(get_chat_session)
):
    try:
        if not request.messages:
            raise HTTPException(status_code=400, detail="消息列表不能为空")
        
        last_user_message = None
        for msg in reversed(request.messages):
            if msg.role == "user":
                last_user_message = _extract_text_from_content(msg.content)
                break

        if not last_user_message or not last_user_message.strip():
            raise HTTPException(status_code=400, detail="用户查询内容不能为空")

        session_id = request.session_id
        if not session_id:
            session_id = session_manager.create_session("新对话")
            logger.info(f"自动创建新会话: {session_id}")

        logger.info(f"收到请求 - 会话ID: {session_id}, 消息数: {len(request.messages)}")

        content_str = _serialize_content(last_user_message)
        session_manager.add_message(
            session_id=session_id,
            role="user",
            content=content_str,
            use_rag=0
        )

        def event_generator():
            try:
                full_response = []
                has_image = False
                
                for chunk in agent.execute_stream(last_user_message):
                    full_response.append(chunk)

                    is_image_url = chunk.startswith("http") and any(ext in chunk.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp'])

                    if is_image_url:
                        has_image = True
                        stream_data = {
                            "type": "image",
                            "image_url": chunk,
                            "isStreaming": False,
                            "progress": 100,
                            "session_id": session_id
                        }
                    else:
                        stream_data = {
                            "type": "text",
                            "content": chunk,
                            "isStreaming": True,
                            "progress": 0,
                            "session_id": session_id
                        }

                    yield f"data: {json.dumps(stream_data, ensure_ascii=False)}\n\n"

                assistant_response = "".join(full_response)
                content_for_db = _build_content_for_db(assistant_response, has_image)
                session_manager.add_message(
                    session_id=session_id,
                    role="assistant",
                    content=content_for_db,
                    use_rag=0
                )

                yield f"data: {json.dumps({'type': 'complete', 'content': '', 'isComplete': True, 'session_id': session_id}, ensure_ascii=False)}\n\n"
                yield "data: [DONE]\n\n"

            except Exception as e:
                logger.error(f"Agent执行错误: {str(e)}", exc_info=True)
                error_data = {
                    "type": "error",
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
    try:
        messages = session_manager.get_history(session_id, limit)
        parsed_messages = [_parse_message_content(msg) for msg in messages]
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "session_id": session_id,
                "history": parsed_messages,
                "total": len(parsed_messages)
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


# ==================== 辅助函数 ====================

def _serialize_content(content) -> str:
    """将内容序列化为JSON字符串存储"""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        return json.dumps([item.dict() for item in content], ensure_ascii=False)
    return str(content)


def _parse_message_content(message: dict) -> dict:
    """解析消息内容，支持图文混合"""
    content = message.get("content", "")
    try:
        if isinstance(content, str) and (content.startswith("[") or content.startswith("{")):
            parsed = json.loads(content)
            if isinstance(parsed, list):
                return {
                    "role": message.get("role"),
                    "content": parsed
                }
    except (json.JSONDecodeError, AttributeError):
        pass
    
    return {
        "role": message.get("role"),
        "content": content
    }


def _extract_text_from_content(content) -> str:
    """从内容中提取纯文本用于LLM处理"""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        texts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    texts.append(item.get("text", ""))
                elif item.get("type") == "image" and item.get("description"):
                    texts.append(f"[图片: {item.get('description')}]")
            elif hasattr(item, 'type'):
                if item.type == "text":
                    texts.append(item.text)
                elif item.type == "image" and item.description:
                    texts.append(f"[图片: {item.description}]")
        return " ".join(texts)
    return str(content)


def _build_content_for_db(response_text: str, has_image: bool) -> str:
    """构建数据库存储的内容格式"""
    if not has_image:
        return response_text

    content_items = []
    current_text = []

    lines = response_text.split('\n')
    for line in lines:
        line_stripped = line.strip()
        if _is_image_url(line_stripped):
            if current_text:
                content_items.append({
                    "type": "text",
                    "text": "\n".join(current_text).strip()
                })
                current_text = []
            content_items.append({
                "type": "image",
                "image_url": line_stripped
            })
        else:
            current_text.append(line)
    
    if current_text:
        content_items.append({
            "type": "text",
            "text": "\n".join(current_text).strip()
        })
    if len(content_items) == 1 and content_items[0]["type"] == "text":
        return content_items[0]["text"]
    return json.dumps(content_items, ensure_ascii=False)

def _is_image_url(text: str) -> bool:
    """判断文本是否为图片URL"""
    if not text or not isinstance(text, str):
        return False
    text_lower = text.lower()
    if not text_lower.startswith(("http://", "https://")):
        return False
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg']
    return any(ext in text_lower for ext in image_extensions)
