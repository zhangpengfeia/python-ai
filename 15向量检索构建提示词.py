"""
提示词: 用户的提问 + 向量库中检索到的参考资料
"""

from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_ollama import OllamaLLM

# 初始化通义千问大模型
model = OllamaLLM(model="qwen3:4b")

# 构建对话提示模板
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:{context}。"),
        ("user", "用户提问: {input}")
    ]
)

# 初始化内存向量库（使用通义千问文本嵌入模型）
vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(model="text-embedding-v4"))

# 传入一个list[str]
vector_store.add_texts(['减肥就是要少吃多练', "在减脂期间吃的东西很重要", "跑步很不错"])
input_text = "怎么减肥？"

# 检索向量库
result = vector_store.similarity_search(input_text, 2)
reference_text = "["
for doc in result:
    reference_text += doc.page_content
reference_text += "]"

def print_prompt(full_prompt):
    """打印拼接后的完整提示词"""
    print("=" * 20, "完整提示词", "=" * 20)
    print(full_prompt.to_string())
    print("=" * 50)
    return full_prompt

def format_func(docs: list[Document]):
    if not docs:
        return "无相关参考资料"
    formatted_str="["
    for doc in docs:
        formatted_str += doc.page_content
    formatted_str += "]"
    return formatted_str

retriever = vector_store.as_retriever(search_kwargs={"k":2})

chain = (
    {"input": RunnablePassthrough(), "context": retriever | format_func} | prompt | print_prompt | model | StrOutputParser()
)

res = chain.invoke(input_text)

print(res)




