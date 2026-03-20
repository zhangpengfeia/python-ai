from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableLambda, RunnableWithMessageHistory
from langchain_ollama import OllamaLLM

model = OllamaLLM(model="qwen3:4b")



# 创建解析器
str_parser = StrOutputParser()

# prompt_template = PromptTemplate.from_template(
#     "你需要根据历史消息回应用户问题，对话历史：{chat_history}，用户提问: {input},请回答：")
prompt = ChatPromptTemplate.from_messages([
    ("system", "你需要根据历史回应用户问题，要简洁回答问题，对话历史："),
    MessagesPlaceholder("chat_history"),
    ("human", "请回答如下问题:{input}")
])

store = {}  # key就是session, value是InMemoryChatMessageHistory对象

def get_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    return store[session_id]

def print_prompt(full_prompt):
    print("="*20, full_prompt.to_string(), "="*20)
    return full_prompt

base_chain = prompt | print_prompt | model | str_parser

converstion_chain: RunnableWithMessageHistory = RunnableWithMessageHistory(
    base_chain,  # 被增强的原有chain
    get_history,  # 通过会话id获取InMemoryChatMessageHistory类对象
    input_messages_key="input",  # 表示用户输入在模板中的占位符
    history_messages_key="chat_history"  # 表示用户输入在模板中的占位符
)

if __name__ == '__main__':
    session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }
    converstion_chain.invoke({"input": "小明有2只猫"}, session_config)
    converstion_chain.invoke({"input": "小红有3只猫"}, session_config)
    converstion_chain.invoke({"input": "小李有8只猫"}, session_config)
    res = converstion_chain.invoke({"input": "总共几只猫"}, session_config)
    print(res)

