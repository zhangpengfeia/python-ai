from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

@tool(description="获取天气")
def get_weather() -> str:
    """获取天气"""
    return "天气晴朗"

agent = create_agent(
    model=ChatOllama(model="qwen3:4b"),
    tools=[get_weather],
    system_prompt="你是一个聊天助手，可以回答用户问题"
)

res = agent.invoke({
    "messages": [
        {"role": "user", "content": "上海天气如何？"}
    ]
})

print(res)
for msg in res["messages"]:
    print(type(msg).__name__, msg.content)
