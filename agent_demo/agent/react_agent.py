from typing import Generator

from langchain.agents import create_agent
from langchain.agents import create_agent
# 工具导入（已正确）
from agent.tools.agent_tools import rag_summarize, get_weather, get_user_location, get_user_id, fetch_external_data,fill_context_for_report, get_current_month
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch
# 模型导入（已正确）
from model.factory import chat_model
# ✅ 修复这一行：去掉 ..
from utils.prompt_loader import load_system_prompts

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
            ],
            middleware=[monitor_tool, log_before_model, report_prompt_switch]
        )

        # ✅ 修复：同步流式方法（适配本地测试，真正逐token输出）

    def execute_stream(self, query: str) -> Generator[str, None, None]:
        input_dict = {
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ]
        }
        # 核心修复1：使用stream_mode="messages" 实现token级流式输出
        # 该模式会在模型生成每个token时实时返回，实现打字机效果
        for token, metadata in self.agent.stream(
                input_dict,
                stream_mode="messages",
                context={"report": False}
        ):
            # 过滤：只保留模型生成的文本内容，过滤工具调用的中间chunk
            if hasattr(token, "content") and token.content.strip():
                # 核心修复2：去掉strip和换行，只返回原生的token增量，不破坏流式连贯性
                yield token.content


if __name__ == '__main__':
    agent = ReactAgent()
    for chunk in agent.execute_stream("扫地机器人在所在的地区气温如何保养？"):
        print(chunk, end="", flush=True)
