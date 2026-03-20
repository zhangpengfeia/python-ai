import json
import os
from typing import Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_ollama import OllamaLLM


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id  # 会话id
        self.storage_path = storage_path  # 存储文件路径
        # 完整路径（拼接为 存储目录/会话id 文件）
        self.file_path = os.path.join(storage_path, self.session_id)
        # 确保存储目录存在
        os.makedirs(self.storage_path, exist_ok=True)

    def add_message(self, message: BaseMessage) -> None:
        """修复核心问题：接收单个BaseMessage，而非Sequence"""
        # 获取已有消息列表
        all_messages = list(self.messages)
        # 单个消息用append（而非extend）
        all_messages.append(message)
        # 将消息转为字典格式
        new_messages = [message_to_dict(msg) for msg in all_messages]
        # 写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f, ensure_ascii=False)  # 保留中文

    @property
    def messages(self) -> list[BaseMessage]:
        """读取并解析本地文件中的消息"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            # 文件不存在时返回空列表
            return []

    def clear(self) -> None:
        """清空会话历史"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)


# 初始化模型
model = OllamaLLM(model="qwen3:4b")

# 创建输出解析器
str_parser = StrOutputParser()

# 构建对话提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你需要根据历史消息回应用户问题，回答要简洁准确。"),
    MessagesPlaceholder("chat_history"),  # 会话历史占位符
    ("human", "{input}")  # 用户输入占位符
])


# 定义获取会话历史的函数
def get_history(session_id):
    """根据session_id获取对应的文件存储会话历史"""
    return FileChatMessageHistory(session_id, './chat_history')


# 定义打印提示词的中间函数（用于调试）
def print_prompt(full_prompt):
    """打印拼接后的完整提示词"""
    print("=" * 20, "完整提示词", "=" * 20)
    print(full_prompt.to_string())
    print("=" * 50)
    return full_prompt


# 构建基础链
base_chain = prompt | print_prompt | model | str_parser

# 包装为带会话记忆的链
conversation_chain: RunnableWithMessageHistory = RunnableWithMessageHistory(
    base_chain,
    get_session_history=get_history,  # 注意参数名是get_session_history（不是get_history）
    input_messages_key="input",  # 用户输入的key
    history_messages_key="chat_history"  # 会话历史的key
)

if __name__ == '__main__':
    # 会话配置（指定session_id）
    session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }

    # 多轮对话测试
    res1 = conversation_chain.invoke({"input": "小明有2只猫"}, config=session_config)
    print("AI回复1：", res1)

    res2 = conversation_chain.invoke({"input": "小红有3只猫"}, config=session_config)
    print("AI回复2：", res2)

    res3 = conversation_chain.invoke({"input": "小李有8只猫"}, config=session_config)
    print("AI回复3：", res3)

    res4 = conversation_chain.invoke({"input": "他们总共有几只猫？"}, config=session_config)
    print("最终答案：", res4)