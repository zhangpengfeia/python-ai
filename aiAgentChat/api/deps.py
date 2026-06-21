# 依赖注入（认证、授权等）
from fastapi import Depends
from agent.react_agent import ReactAgent
from typing import Optional

# 单例模式：全局只初始化一次Agent，避免重复创建
_agent_instance: Optional[ReactAgent] = None

def get_agent() -> ReactAgent:
    """
    获取Agent实例（单例模式，全局复用）
    """
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = ReactAgent()
    return _agent_instance