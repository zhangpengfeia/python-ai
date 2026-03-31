from langchain.agents import create_agent
from langchain.agents import create_agent
# 工具导入（已正确）
from agent.tools.agent_tools import rag_summarize, get_weather, get_user_location, get_user_id, fetch_external_data,fill_context_for_report, get_current_month
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
            middleware=[]
        )

    def execute_stream(self, query: str):
        input_dict = {
            "messages":[
                {
                    "role": "user",
                    "content": query
                }
            ]
        }
        # context就是上下文runtime中的信息，就是提示词切换的标记
        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                yield latest_message.content.strip() + "\n"

if __name__ == '__main__':
    agent = ReactAgent()
    for chunk in agent.execute_stream("扫地机器人在所在的地区气温如何保养？"):
        print(chunk, end="", flush=True)
