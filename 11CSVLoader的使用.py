from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path="./data/stu.csv",
    encoding="utf-8",
    csv_args={
        "delimiter": ",",
        "quotechar": '"',
        # 数据原本有表头，就不要写夏某代码，如果没有可以用
        "fieldnames": ["name", "age"],
    }
)
documents = loader.load()

for document in documents:
    print(document)