from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_ollama import OllamaLLM

example_template = PromptTemplate.from_template("单词:{word}, 反义词：{antonym}")

examples_data = [
    {"word": "大", "antonym": "小"}
]

few_shot_template = FewShotPromptTemplate(
    example_prompt=example_template, # 示例数据的模板
    examples=examples_data, # 示例的数据（用来注入动态数据），list内套字典
    prefix="告诉我单词的反义词，我提供如下的示例", # 示例之前的提示词
    suffix="基于前面的示例告诉我，{input_word} 的反义词是什么？", # 示例之后的提示词
    input_variables=['input_word'] # 声明在前缀或后缀中所需要注入的变量名
)

prompt_text = few_shot_template.invoke(input={"input_word": "不三不四"})

model = OllamaLLM(model="qwen3:4b")

res = model.stream(input=prompt_text)

for chunk in res:
    print(chunk, end="", flush=True)
