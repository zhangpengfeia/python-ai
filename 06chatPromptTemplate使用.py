from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableSerializable
from langchain_ollama import OllamaLLM

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是英雄联盟专业知识库，了解所有英雄。"),
        MessagesPlaceholder("history"),
        ("human", "请在描述一个英雄")
    ]
)
history_data = [
    ("human", "你来随机描述一个英雄"),
    ("ai", "李青，特征是瞎子"),
    ("human", "请在描述一个"),
    ("ai", "蛮王,不穿上衣")
]
model = OllamaLLM(model="qwen3:4b")

chain: RunnableSerializable = chat_prompt_template | model

res = chain.invoke({"history": history_data})

print(res)

for chunk in chain.stream({"history": history_data}):
    print(chunk, end="", flush=True)

