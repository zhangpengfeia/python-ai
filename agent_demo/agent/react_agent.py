from typing import Generator
from langchain_core.messages import BaseMessage, AIMessageChunk
from langchain.agents import create_agent
from agent.tools.agent_tools import rag_summarize, get_weather, get_user_location, get_user_id, fetch_external_data, \
    fill_context_for_report, get_current_month, generate_image_from_text
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch
from model.factory import chat_model
from utils.prompt_loader import load_system_prompts

import re

# 简单正则匹配图片 URL（可根据你的实际 URL 格式微调）
IMAGE_URL_PATTERN = re.compile(
    r'https?://[^\s]+?\.(png|jpg|jpeg|gif|bmp|webp)(\?.*)?$',
    re.IGNORECASE
)

class ReactAgent:
    def __init__(self):
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
                generate_image_from_text  # 画图工具
            ],
            middleware=[monitor_tool, log_before_model, report_prompt_switch]
        )

    async def execute_stream_async(self, query: str):
        input_dict = {
            "messages": [
                {"role": "user", "content": query}
            ]
        }
        async for event in self.agent.astream_events(input_dict, version="v2", stream_mode="messages", context={"report": False}):
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

        # 用来缓存完整内容，判断是否是图片 URL
        full_content = []

        for chunk in self.agent.stream(input_dict, stream_mode="messages", context={"report": False}):
            token, metadata = chunk
            if isinstance(token, AIMessageChunk) and token.content:
                full_content.append(token.content)

        # 拼接完整结果
        final_output = "".join(full_content).strip()

        # ====================== 核心判断 ======================
        if IMAGE_URL_PATTERN.match(final_output):
            # 如果是图片 URL → 不流式，一次性返回
            yield final_output
        else:
            # 正常文本 → 流式返回
            for part in full_content:
                yield part


if __name__ == '__main__':
    agent = ReactAgent()
    # query = "扫地机器人在所在的地区气温如何保养？"
    query = "画一只小猫"  # 测试图片URL → 会一次性返回
    for chunk in agent.execute_stream(query):
        print(chunk, end="", flush=True)