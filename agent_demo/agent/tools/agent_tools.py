# agent 工具
import os

from langchain_core.tools import tool

from agent.tools.api_image_generation import api_image_from_text
from rag.rag_service import RagSummarizeService
from utils.config_handler import agent_conf
from utils.logger_handler import logger
from utils.path_tool import get_abs_path
from agent.tools.api_user_location import api_city
from agent.tools.api_weather import api_weather
from datetime import datetime

rag = RagSummarizeService()
external_data = {}

@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)

@tool(description="获取当前城市天气,消息字符串形式返回")
def get_weather() -> str:
    city_info = api_city()
    weather = api_weather(city_info["location_id"])
    return weather

@tool(description="获取用户所在城市名称，字符串形式返回")
def get_user_location() -> str:
    # 执行获取
    city_info = api_city()
    return city_info

@tool(description="获取用户id")
def get_user_id() -> str:
    return "1003"

@tool(description="获取用户当前月份，字符串形式返回")
def get_current_month() -> str:
    return datetime.now().strftime("%Y-%m")

def generate_external_data():
    if not external_data:
        external_data_path = get_abs_path(agent_conf["external_data_path"])
        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件{external_data_path}不存在")
        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr: list[str] = line.strip().split(",")
                user_id: str = arr[0].replace('"', "")
                feature: str = arr[1].replace('"', "")
                efficiency: str = arr[2].replace('"', "")
                consumables: str = arr[3].replace('"', "")
                comparison: str = arr[4].replace('"', "")
                time: str = arr[5].replace('"', "")
                if user_id not in external_data:
                    external_data[user_id] = {}
                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison,
                }

@tool(description="从外部系统中获取指定用户指定月份的使用记录，以字符串像是返回，为检索则返回空字符串")
def fetch_external_data(user_id: str, moth: str) -> str:
    generate_external_data()
    try:
        return external_data[user_id][moth]
    except KeyError:
        logger.warning(f"[外部数据] 未找到用户{user_id}的{moth}月数据")

@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    return "fill_context_for_report已调用"

@tool(description="根据文本描述生成图像，size 默认格式为2048*2048,只返回图片链接，不需要任何文字信息")
def generate_image_from_text(prompt: str, negative_prompt: str = "", size: str = "2048*2048") -> str:
    return api_image_from_text(prompt, negative_prompt, size)


if __name__ == "__main__":
    print(fetch_external_data("1001", "2025-01"))

