from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

prompt_template = PromptTemplate.from_template("我的邻居姓{name},生了{gender},帮我起个名字")

prompt_text = prompt_template.format(name='张', gender="女")
print(prompt_text)

model = OllamaLLM(model="qwen3:4b")

res = model.stream(input=prompt_text)

for chunk in res:
    print(chunk, end="", flush=True)
