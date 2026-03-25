from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import OllamaLLM

import config_data as config
from vector_stores import VectorStoreService

def print_prompt(full_prompt):
    """打印拼接后的完整提示词"""
    print("="*20)
    print(full_prompt.to_string())
    print("="*20)
    return full_prompt

class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreService(DashScopeEmbeddings(model=config.embedding_model_name))
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考资料为主," "简洁和专业的语句回答。参考资料:{context}。"),
                ("user", "请回答用户提问:{input}")
            ]
        )
        self.chat_model = OllamaLLM(model=config.chat_model_name)
        self.chain = self.__get_chain()

    def __get_chain(self):
        retriever = self.vector_service.get_retriever()

        def format_document(docs: list[Document]):
            if not docs:
                return "无相关参考资料"
            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段:{doc.page_content}\n文档元数据：{doc.metadata}\n\n"

            return formatted_str
        chain = (
            {
                "input": RunnablePassthrough(),
                "context": retriever | format_document
            } | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )
        return chain
if __name__ == "__main__":
    r = RagService().chain.invoke("平台简介?")
    print(r)