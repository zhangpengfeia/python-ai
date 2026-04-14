from typing import Generator
from langchain_core.messages import BaseMessage, AIMessageChunk
from langchain.agents import create_agent
from agent.tools.agent_tools import rag_summarize, get_weather, get_user_location, get_user_id, fetch_external_data, \
    fill_context_for_report, get_current_month, generate_image_from_text
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch
from model.factory import chat_model
from utils.prompt_loader import load_system_prompts

import re

IMAGE_URL_PATTERN = re.compile(
    r'https?://[^\s)]+?\.(png|jpg|jpeg|gif|bmp|webp)(\?[^\s)]*)?',
    re.IGNORECASE
)

MARKDOWN_IMAGE_PATTERN = re.compile(
    r'!\[.*?\]\((https?://[^\s)]+?\.(png|jpg|jpeg|gif|bmp|webp)(\?[^\s)]*)?)\)',
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
                generate_image_from_text
            ],
            middleware=[monitor_tool, log_before_model, report_prompt_switch]
        )

    async def execute_stream_async(self, query: str):
        input_dict = {
            "messages": [
                {"role": "user", "content": query}
            ]
        }
        
        full_content = []
        is_image_generation = False
        
        async for event in self.agent.astream_events(input_dict, version="v2", stream_mode="messages", context={"report": False, "is_image_generation": False}):
            if event["event"] == "on_chat_model_stream":
                chunk = event["data"]["chunk"]
                if chunk.content:
                    full_content.append(chunk.content)
            
            if event["event"] == "on_chain_end":
                if hasattr(event, 'metadata') and event.get('metadata', {}).get('context'):
                    is_image_generation = event['metadata']['context'].get('is_image_generation', False)
        
        final_output = "".join(full_content).strip()
        
        markdown_match = MARKDOWN_IMAGE_PATTERN.search(final_output)
        if markdown_match:
            yield markdown_match.group(1)
            return
        
        image_url_match = IMAGE_URL_PATTERN.search(final_output)
        if image_url_match:
            yield image_url_match.group(0)
            return
        
        for part in full_content:
            yield part

    def execute_stream(self, query: str) -> Generator[str, None, None]:
        input_dict = {
            "messages": [
                {"role": "user", "content": query}
            ]
        }

        full_content = []
        context = {"report": False, "is_image_generation": False}

        for chunk in self.agent.stream(input_dict, stream_mode="messages", context=context):
            token, metadata = chunk
            if isinstance(token, AIMessageChunk) and token.content:
                full_content.append(token.content)

        final_output = "".join(full_content).strip()
        
        is_image_generation = context.get("is_image_generation", False)

        if is_image_generation:
            print(f"\n[检测到图像生成工具被调用]")
            markdown_match = MARKDOWN_IMAGE_PATTERN.search(final_output)
            if markdown_match:
                print(f"[提取到Markdown格式图片链接]")
                yield markdown_match.group(1)
                return
            
            image_url_match = IMAGE_URL_PATTERN.search(final_output)
            if image_url_match:
                print(f"[提取到普通图片链接]")
                yield image_url_match.group(0)
                return

        print(f"\n[普通文本流式输出]")
        for part in full_content:
            yield part


if __name__ == '__main__':
    agent = ReactAgent()
    print("="*60)
    print("测试1: 图像生成 - 应该一次性返回纯URL")
    print("="*60)
    query = "画一只小猫"
    print(f"用户输入: {query}")
    print("-"*60)
    result_chunks = []
    for chunk in agent.execute_stream(query):
        result_chunks.append(chunk)
        print(f"输出片段: {repr(chunk)}")
    print(f"\n完整结果: {''.join(result_chunks)}")
    print(f"是否为纯URL: {result_chunks and len(result_chunks) == 1 and IMAGE_URL_PATTERN.match(result_chunks[0])}")
    print("\n" + "="*60)
