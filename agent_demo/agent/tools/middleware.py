from idlelib.undo import Command
from typing import Callable

from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain_core.messages import ToolMessage
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.runtime import Runtime
from agent_demo.utils.logger_handler import logger
from agent_demo.utils.prompt_loader import load_report_prompts, load_system_prompts

# 工具执行的监控
@wrap_tool_call
def monitor_tool(
    # 请求数据的封装
    request: ToolCallRequest,
    # 执行的函数本身
    handler: Callable[[ToolCallRequest], ToolMessage | Command]
) -> ToolMessage | Command:
    # 自定义逻辑
    logger.info(f"[工具执行] 工具：{request.tool_call.name}")
    logger.info(f"[工具执行] 参数：{request.tool_call.args}")
    # 原封不动返回
    try:
        res = handler(request)
        logger.info(f"[工具执行] 结果：{request.tool_call.name} 调用成功")

        # 当工具类 fill_context_for_report 返回，则将 report 设置为 True
        if res.tool_call['name'] == "fill_context_for_report":
            request.runtime.context["report"] = True
        return res
    except Exception as e:
        logger.error(f"[工具执行] 错误：{request.tool_call.name} 调用失败，{str(e)}")
        raise e

@before_model
def log_before_model(
        state: AgentState,  # 整个Agent智能体中的状态记录
        runtime: Runtime # 记录整个执行过程中的上下文信息
) -> str:
    logger.info(f"[Before model]即将模型调用，并附带{len(state['messages'])}消息")
    logger.debug(f"[Before model]{type(state['messages'][-1]).__name__} | {state['messages'[-1].content.strip()]}")
    # 中间件不需要返回值
    return None

# 动态切换提示词
@dynamic_prompt # 每一次在生成提示词之前，调用此函数
def report_prompt_switch(request: ModelRequest):
    is_report = request.runtime.context.get("report", False)
    if is_report: # 是报告生成场景，返回报告生成提示词内容
        return load_report_prompts()
    return load_system_prompts()
