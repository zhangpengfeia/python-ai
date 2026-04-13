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

# 图像工厂
class ChatImageFactory(BaseModelFactory):
    def __init__(self, model_name: str = "qwen-image-2.0", size: str = "2048*2048"):
        self.model_name = model_name
        self.size = size
        dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
    
    def generator(self) -> Optional[Dict[str, Any]]:
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            raise ValueError("DASHSCOPE_API_KEY environment variable is not set")
        
        return {
            "model": self.model_name,
            "size": self.size,
            "api_key": api_key
        }
    
    def generate_image(self, prompt: str, negative_prompt: str = "", 
                      stream: bool = False, watermark: bool = False,
                      prompt_extend: bool = True) -> Dict[str, Any]:
        messages = [
            {
                "role": "user",
                "content": [
                    {"text": prompt}
                ]
            }
        ]
        
        call_params = {
            "model": self.model_name,
            "messages": messages,
            "result_format": 'message',
            "stream": stream,
            "watermark": watermark,
            "prompt_extend": prompt_extend,
            "size": self.size
        }
        
        if negative_prompt:
            call_params["negative_prompt"] = negative_prompt
        
        response = MultiModalConversation.call(**call_params)
        
        if response.status_code == 200:
            return {
                "success": True,
                "data": json.loads(json.dumps(response, ensure_ascii=False))
            }
        else:
            return {
                "success": False,
                "error": {
                    "status_code": response.status_code,
                    "code": response.code,
                    "message": response.message
                }
            }


chat_model = ChatModelFactory().generator()
chat_oll_model = ChatOllamaModelFactory().generator()
embed_model = EmbeddingFactory().generator()
image_model = ChatImageFactory()

if __name__ == '__main__':
    res = chat_oll_model.stream(input="你是谁？")
    for chunk in res:
        print(chunk, end="", flush=True)




