from typing import Generator
from langchain_core.messages import BaseMessage, AIMessageChunk
from langchain.agents import create_agent
from agent.tools.agent_tools import rag_summarize, get_weather, get_user_location, get_user_id, fetch_external_data, \
    fill_context_for_report, get_current_month
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch
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
        input_dict = {
            "messages": [
                {"role": "user", "content": query}
            ]
        }
        for chunk in self.agent.stream(input_dict,stream_mode="messages",context={"report": False}):
            token, metadata = chunk
            if isinstance(token, AIMessageChunk) and token.content:
                yield token.content

if __name__ == '__main__':
    agent = ReactAgent()
    query = "扫地机器人在所在的地区气温如何保养？"
    for chunk in agent.execute_stream(query):
        print(chunk, end="", flush=True)
