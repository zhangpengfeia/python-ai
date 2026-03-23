from langchain_community.document_loaders import JSONLoader

loader = JSONLoader(
    file_path="./data/stus.json",
    jq_schema=".[].name",  # 正确语法：遍历数组元素，提取 name 字段
    text_content=False
)

document = loader.load()
print(document)