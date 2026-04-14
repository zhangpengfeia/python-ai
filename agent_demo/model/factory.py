from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import json

from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_ollama import OllamaLLM, ChatOllama
import dashscope
from dashscope import MultiModalConversation

from utils.config_handler import rag_conf
import os

# 模型工厂
class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass

# 聊天模型工厂
class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatTongyi(model=rag_conf["chat_model_name"])

# 嵌入模型工厂
class EmbeddingFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(
            model=rag_conf['embedding_model_name']
        )
# 聊天模型工厂
class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatTongyi(model=rag_conf["chat_model_name"], streaming=True)

class ChatOllamaModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatOllama(model=rag_conf["chat_oll_model_name"],  streaming=True) # 启用流式输出

chat_model = ChatModelFactory().generator()
chat_oll_model = ChatOllamaModelFactory().generator()
embed_model = EmbeddingFactory().generator()

if __name__ == '__main__':
    res = chat_oll_model.stream(input="你是谁？")
    for chunk in res:
        print(chunk, end="", flush=True)




