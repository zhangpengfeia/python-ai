from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

@tool(description="获取天气")
def get_weather(name: str) -> str:
    """获取天气"""
    return f"{name}：天气晴朗"

def get_temperature(name: str) -> str:
    """获取天气"""
    return f"{name}：温度为19°"


agent = create_agent(
    model=ChatOllama(model="qwen3:4b"),
    tools=[get_weather,get_temperature],
    system_prompt="""你是严格遵循 ReAct 框架的智能体，必须按「思考→行动→观察→再思考」的流程解决问题，且**每轮仅能思考并调用 1 个工具**，禁止单次调用多个工具。
并告知我你的思考过程，工具的调用原因，按思考、行动、观察三个结构告知我"""
)

res_stream = agent.stream(
    { "messages": [ {"role": "user", "content": "上海天气如何,多少度？"}]},
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

