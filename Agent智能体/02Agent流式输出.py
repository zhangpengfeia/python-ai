from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

@tool(description="获取天气")
def get_weather(name: str) -> str:
    """获取天气"""
    return f"{name}：天气晴朗"

agent = create_agent(
    model=ChatOllama(model="qwen3:4b"),
    tools=[get_weather],
    system_prompt="你是一个聊天助手，可以回答用户问题"
)

res_stream = agent.stream(
    { "messages": [ {"role": "user", "content": "上海天气如何？"}]},
    stream_mode="values"
)

for chunk in res_stream:
    latest_mes = chunk['messages'][-1]
    if latest_mes.content:
        print(type(latest_mes).__name__,latest_mes.content)
    try:
        if latest_mes.tool_calls:
            print(f"工具调用：{[tc['name'] for tc in latest_mes.tool_calls]}")
    except AttributeError as e:
        pass

