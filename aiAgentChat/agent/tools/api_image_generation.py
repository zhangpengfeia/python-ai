from langchain_core.tools import tool
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rag.rag_image import image_service

def api_image_from_text(prompt: str, negative_prompt: str = "", size: str = "2048*2048") -> str:
    """
    根据用户的文本描述生成图像
    Args:
        prompt: 图像描述文本
        negative_prompt: 负向提示词（可选，为空则使用配置文件中的默认值）
        size: 图像尺寸（可选，为空则使用配置文件中的默认值，如：2048*2048、1024*1024）
    Returns:
        图片URL地址（纯URL，不含其他文字）
    """
    result = image_service.generate_image(
        prompt=prompt,
        negative_prompt=negative_prompt if negative_prompt else None,
        size=size if size else None
    )

    if result["success"]:
        image_url = result["data"]["image_url"]
        if image_url:
            return image_url
        else:
            return "ERROR: 图像生成成功但未能获取图片URL"
    else:
        return f"ERROR: 图像生成失败 - {result['error']}"
