

import json
import os

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict


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

