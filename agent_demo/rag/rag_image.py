import json
import os
import dashscope
from dashscope import MultiModalConversation
from typing import Optional, Dict, Any
from utils.config_handler import rag_conf

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'


class QwenImageService:
    """通义千问图像生成服务"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY 环境变量未设置")
        
        self.image_config = rag_conf.get("image_generation", {})
        self.default_size = self.image_config.get("default_size", "2048*2048")
        self.default_negative_prompt = self.image_config.get(
            "negative_prompt",
            "低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。"
        )
        self.model = self.image_config.get("model", "qwen-image-2.0")
        self.prompt_extend = self.image_config.get("prompt_extend", True)
        self.watermark = self.image_config.get("watermark", False)
        self.stream = self.image_config.get("stream", False)

    def generate_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        size: Optional[str] = None,
        stream: Optional[bool] = None,
        watermark: Optional[bool] = None,
        prompt_extend: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        根据文本描述生成图像

        Args:
            prompt: 图像描述文本
            negative_prompt: 负向提示词，默认从配置读取
            size: 图像尺寸，默认从配置读取（如：2048*2048）
            stream: 是否流式返回，默认从配置读取
            watermark: 是否添加水印，默认从配置读取
            prompt_extend: 是否启用提示词扩展，默认从配置读取

        Returns:
            包含生成结果的字典，格式为：
            {
                "success": bool,
                "data": {
                    "image_url": str | None,
                    "raw_response": dict | None
                },
                "error": str | None
            }
        """
        messages = [
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ]

        try:
            response = MultiModalConversation.call(
                model=self.model,
                messages=messages,
                result_format='message',
                stream=stream if stream is not None else self.stream,
                watermark=watermark if watermark is not None else self.watermark,
                prompt_extend=prompt_extend if prompt_extend is not None else self.prompt_extend,
                negative_prompt=negative_prompt if negative_prompt is not None else self.default_negative_prompt,
                size=size if size is not None else self.default_size
            )

            if response.status_code == 200:
                image_url = self._extract_image_url(response.output)
                return {
                    "success": True,
                    "data": {
                        "image_url": image_url,
                        "raw_response": json.loads(json.dumps(response.output, ensure_ascii=False))
                    },
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "data": {
                        "image_url": None,
                        "raw_response": None
                    },
                    "error": f"HTTP返回码：{response.status_code}, 错误码：{response.code}, 错误信息：{response.message}"
                }

        except Exception as e:
            return {
                "success": False,
                "data": {
                    "image_url": None,
                    "raw_response": None
                },
                "error": f"图像生成异常：{str(e)}"
            }

    def _extract_image_url(self, output: Dict[str, Any]) -> Optional[str]:
        """
        从响应中提取图像URL
        Args:
            output: API响应的output字段
            
        Returns:
            图像URL，如果提取失败则返回None
        """
        try:
            choices = output.get("choices", [])
            if choices and len(choices) > 0:
                message = choices[0].get("message", {})
                content = message.get("content", [])
                if content and len(content) > 0:
                    return content[0].get("image")
        except Exception:
            pass
        return None


image_service = QwenImageService()


if __name__ == '__main__':
    test_prompt = "生成一只可爱的小猫"
    result = image_service.generate_image(prompt=test_prompt)
    if result["success"]:
        image_url = result["data"]["image_url"]
        print(f"图片地址: {image_url}")

        # 如需原始完整响应
        raw_data = result["data"]["raw_response"]
