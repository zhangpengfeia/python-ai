import sys
from pathlib import Path

# 把agent_demo根目录加入搜索路径
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
from chat_session import ChatSession
from vector_store import VectorStoreService

# 初始化
session = ChatSession()
vs = VectorStoreService()

# 1. 创建一个新会话
sid = session.create_session(session_name="设备维护咨询")
print("新会话ID:", sid)

# 2. 用户提问
user_query = "设备日常怎么维护？"
session.add_message(session_id=sid, role="user", content=user_query)

# 3. 获取历史上下文（给大模型做记忆）
history = session.get_history(sid, limit=10)
context = [{"role": h["role"], "content": h["content"]} for h in history]

# 4. RAG 检索知识库
retriever = vs.get_retriever()
docs = retriever.invoke(user_query)
rag_content = "\n".join([d.page_content for d in docs])

# 5. 构造 prompt（上下文 + 知识库）
prompt = f"""
上下文历史：
{context}

知识库内容：
{rag_content}

用户问题：{user_query}
请结合知识库回答。
"""

# 6. 调用你的 chat_model 获取回答
from model.factory import chat_model
response = chat_model.invoke(prompt).content

# 7. 保存AI回答
session.add_message(session_id=sid, role="assistant", content=response, use_rag=1)

# 8. 输出
print("AI回答：", response)