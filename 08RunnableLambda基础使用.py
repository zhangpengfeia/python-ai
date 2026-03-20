from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_ollama import OllamaLLM

# 创建解析器
str_parser = StrOutputParser()

model = OllamaLLM(model="qwen3:4b")

prompt_template = PromptTemplate.from_template("我的邻居姓{xingname},生了{gender},帮我起个名字,只需要告诉我名字，不需要任何信息")

second_template = PromptTemplate.from_template("姓名{name},帮我解析含义")

ai_func = RunnableLambda(lambda ai_msg: {"name": ai_msg})

chain = prompt_template | model | ai_func | second_template | model | str_parser

res = chain.stream({"xingname": "李", "gender":"女"})

print(res)
for chunk in res:
    print(chunk, end="", flush=True)
