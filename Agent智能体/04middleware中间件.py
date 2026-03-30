from langchain.agents import create_agent
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, \
    wrap_tool_call
from langchain_ollama import ChatOllama
from langchain_core.tools import tool


@tool(description="获取天气")
def get_weather(city: str) -> str:
    """获取天气"""
    return f"{city}：天气晴朗"

@tool(description="获取温度")
def get_temperature(name: str) -> str:
    """获取天气"""
    return f"{name}：温度为19°"


# 在运行agent之前，执行此函数
@before_agent
def log_before_agent(state: str, runtime: str) -> str:
    print(f"[Before agent]agent启动，并附带{len(state['messages'])}消息")

# agent结束后
@after_agent
def log_after_agent(state: str, runtime: str) -> str:
    print(f"[Before agent]agent结束，并附带{len(state['messages'])}消息")

#model执行前
@before_model
def log_before_model(state: str, runtime: str) -> str:
    print(f"[Before model]model启动模型调用，并附带{len(state['messages'])}消息")

# model执行后
@after_model
def log_after_model(state: str, runtime: str) -> str:
    print(f"[Before model]model结束模型调用，并附带{len(state['messages'])}消息")

# 模型调用中
@wrap_model_call
def model_call_hook(request, handler):
    print("模型调用中")
    return handler(request)

# 工具调用中
@wrap_tool_call
def tool_call_hook(request, handler):
    print(f"工具调用：{request.tool_call['name']}")
    print(f"工具调用参数：{request.tool_call['args']}")
    return handler(request)



agent = create_agent(
    model=ChatOllama(model="qwen3:4b"),
    tools=[get_weather,get_temperature],
    middleware=[
        log_before_agent,
        log_after_agent,
        log_before_model,
        log_after_model,
        model_call_hook,
        tool_call_hook
    ],
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

