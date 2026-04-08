"""
总结服务类： 用户提问。搜索参考资料，将提问和参考资料交给模型，让模型总结回复
"""
import sys
from pathlib import Path
from typing import AsyncGenerator, List, Optional

# 把agent_demo根目录加入搜索路径
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from model.factory import chat_model
from utils.prompt_loader import load_rag_prompts
from rag.vector_store import VectorStoreService


def print_prompt(prompt):
    print("=" * 20)
    print(prompt.to_string())
    print("=" * 20)
    return prompt


class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()

    def _init_chain(self):
        chain = self.prompt_template | print_prompt | self.model | StrOutputParser()
        return chain

    def retriever_docs(self, query: str) -> list[Document]:
        return self.retriever.invoke(query)

    def rag_summarize(self, query: str) -> str:
        """原有非流式方法（保留）"""
        context_docs = self.retriever_docs(query)
        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"【参考资料{counter}】: 参考资料：{doc.page_content} | 参考元数据：{doc.metadata}\n"
        return self.chain.invoke(
            {
                "input": query,
                "context": context,
            }
        )

    # ✅ 新增：流式生成方法
    async def rag_summarize_stream(self, query: str) -> AsyncGenerator[str, None]:
        """
        流式生成 RAG 回复
        Yields: 单个 token 或文本块
        """
        context_docs = self.retriever_docs(query)
        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"【参考资料{counter}】: 参考资料：{doc.page_content} | 参考元数据：{doc.metadata}\n"

        # ✅ 使用 astream 进行流式调用
        async for chunk in self.chain.astream(
                {
                    "input": query,
                    "context": context,
                }
        ):
            if chunk:  # 过滤空块
                yield chunk
if __name__ == '__main__':
    rag = RagSummarizeService()
    print(rag.rag_summarize_stream("小户型适合哪些扫地机器人"))