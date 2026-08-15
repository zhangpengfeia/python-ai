from langchain_core.tools import BaseTool

from langgraph_python.tools.time import get_current_time
from langgraph_python.tools.web import fetch_url, web_search
from langgraph_python.tools.sub_agent import call_sub_agent

_AVAILABLE_TOOLS: dict[str, BaseTool] = {
    "fetch_url": fetch_url,
    "web_search": web_search,
    "get_current_time": get_current_time,
    "call_sub_agent": call_sub_agent,
}

tools: list[BaseTool] = list(_AVAILABLE_TOOLS.values())


def get_tools(names: list[str]) -> list[BaseTool]:
    """根据工具名称列表返回对应的工具函数列表，未知名称会被忽略"""
    return [_AVAILABLE_TOOLS[name] for name in names if name in _AVAILABLE_TOOLS]
