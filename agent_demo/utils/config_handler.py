"""
yaml
k: v
"""
import os
import re
import yaml
from dotenv import load_dotenv

from utils.path_tool import get_abs_path

# 加载环境变量
load_dotenv()


def _resolve_env_vars(value):
    """解析环境变量占位符 ${VAR} 或 ${VAR:default}"""
    if not isinstance(value, str):
        return value
    
    # 匹配 ${VAR} 或 ${VAR:default_value}
    pattern = r'\$\{([^}:]+)(?::([^}]*))?\}'
    
    def replace_match(match):
        var_name = match.group(1)
        default_value = match.group(2)
        env_value = os.getenv(var_name)
        
        if env_value is not None:
            return env_value
        elif default_value is not None:
            return default_value
        else:
            raise ValueError(f"环境变量 '{var_name}' 未设置且没有默认值")
    
    result = re.sub(pattern, replace_match, value)
    
    return result


def _convert_type(value):
    """智能转换配置值的类型"""
    if not isinstance(value, str):
        return value
    
    # 去除首尾空白
    value = value.strip()
    
    # 布尔值转换
    if value.lower() in ('true', 'yes', 'on'):
        return True
    if value.lower() in ('false', 'no', 'off'):
        return False
    
    # 整数转换
    try:
        return int(value)
    except ValueError:
        pass
    
    # 浮点数转换
    try:
        return float(value)
    except ValueError:
        pass
    
    return value


def _process_config(config):
    """递归处理配置中的所有字符串值，解析环境变量并转换类型"""
    if isinstance(config, dict):
        return {key: _process_config(value) for key, value in config.items()}
    elif isinstance(config, list):
        return [_process_config(item) for item in config]
    elif isinstance(config, str):
        resolved = _resolve_env_vars(config)
        return _convert_type(resolved)
    else:
        return config


def load_rag_config(config_path: str=get_abs_path("config/rag.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return _process_config(config)


def load_chroma_config(config_path: str=get_abs_path("config/chroma.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return _process_config(config)


def load_prompts_config(config_path: str=get_abs_path("config/prompts.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return _process_config(config)


def load_agent_config(config_path: str=get_abs_path("config/agent.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return _process_config(config)


def load_db_config(config_path: str=get_abs_path("config/db.yml"), encoding: str="utf-8"):
    """加载数据库配置"""
    with open(config_path, "r", encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return _process_config(config)


rag_conf = load_rag_config()
chroma_conf = load_chroma_config()
prompts_conf = load_prompts_config()
agent_conf = load_agent_config()
db_conf = load_db_config()


if __name__ == '__main__':
    print(rag_conf["chat_model_name"])
    print(db_conf["mysql"]["host"])
    print(db_conf["chroma"]["host"])
    print(f"MySQL 密码已加载: {'*' * len(str(db_conf['mysql']['password']))}")
    print(f"密码类型: {type(db_conf['mysql']['password'])}")
    print(f"端口类型: {type(db_conf['mysql']['port'])}")
