# 阿里通义大模型访问
from langchain_community.llms.tongyi import Tongyi
# ollama 大模型访问
from langchain_ollama import OllamaLLM

model = OllamaLLM(model="qwen3:4b")

res = model.stream(input="你是谁？")

for chunk in res:
    print(chunk, end="", flush=True)


