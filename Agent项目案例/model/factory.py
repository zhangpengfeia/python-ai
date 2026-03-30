from abc import ABC, abstractmethod
from typing import Optional

from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel

from agent项目案例.utils.config_handler import rag_conf
import os

# 模型工厂
class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass

# 聊天模型工厂
class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        api_key = rag_conf.get("api_key") or os.getenv("DASHSCOPE_API_KEY")
        return ChatTongyi(model=rag_conf["chat_model_name"], api_key=api_key)

# 嵌入模型工厂
class EmbeddingFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        api_key = rag_conf.get("api_key") or os.getenv("DASHSCOPE_API_KEY")
        return DashScopeEmbeddings(model=rag_conf['embedding_model_name'], dashscope_api_key=api_key)

chat_model = ChatModelFactory().generator()
embed_model = EmbeddingFactory().generator()

