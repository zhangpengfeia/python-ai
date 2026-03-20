from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_ollama import OllamaLLM

# 创建解析器
str_parser = StrOutputParser()
json_parser = JsonOutputParser()


model = OllamaLLM(model="qwen3:4b")

prompt_template = PromptTemplate.from_template("我的邻居姓{xingname},生了{gender},帮我起个名字,帮我严格输出为json格式,key为name")

second_template = PromptTemplate.from_template("姓名{name},帮我解析含义")

chain = prompt_template | model | json_parser | second_template | model | str_parser

res = chain.stream({"xingname": "张", "gender":"女"})

# print(res)
for chunk in res:
    print(chunk, end="", flush=True)
