import asyncio
from typing import Generator

# LangChain 1.2 流式必须导入
from langchain_core.messages import BaseMessage, AIMessageChunk
from langchain.agents import create_agent

# 工具导入（保持你原来的）
from agent.tools.agent_tools import rag_summarize, get_weather, get_user_location, get_user_id, fetch_external_data, \
    fill_context_for_report, get_current_month
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch
# 模型导入（保持你原来的）
from model.factory import chat_model, chat_oll_model
from utils.prompt_loader import load_system_prompts
class ReactAgent:
    def __init__(self):
        # 你原来的创建方式不变（create_agent 是 LangChain 1.2 官方）
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompts(),
            tools=[
                rag_summarize,
                get_weather,
                get_user_location,
                get_user_id,
                get_current_month,
                fetch_external_data,
                fill_context_for_report,
            ],
            middleware=[monitor_tool, log_before_model, report_prompt_switch]
        )

    async def execute_stream_async(self, query: str):
        """异步流式输出，更可靠的 token 级别流式"""
        input_dict = {
            "messages": [
                {"role": "user", "content": query}
            ]
        }
        async for event in self.agent.astream_events(input_dict, version="v2",stream_mode="messages",context={"report": False}):
            if event["event"] == "on_chat_model_stream":
                chunk = event["data"]["chunk"]
                if chunk.content:
                    yield chunk.content

    def execute_stream(self, query: str) -> Generator[str, None, None]:
        """
        使用 stream_mode="messages" 获取消息级别的流式输出
        """
        input_dict = {
            "messages": [
                {"role": "user", "content": query}
            ]
        }
        # 使用 stream_mode="messages" 启用真正的流式输出
        for chunk in self.agent.stream(input_dict,stream_mode="messages",context={"report": False}):
            token, metadata = chunk
            # 只处理 AI 消息的增量内容
            # 只处理 AI 消息的增量内容
            if isinstance(token, AIMessageChunk) and token.content:
                yield token.content

if __name__ == '__main__':
    agent = ReactAgent()
    query = "扫地机器人在所在的地区气温如何保养？"
    for chunk in agent.execute_stream(query):
        print(chunk, end="", flush=True)
