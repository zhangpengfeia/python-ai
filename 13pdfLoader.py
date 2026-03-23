from langchain_community.document_loaders import PyPDFLoader

pdfloader = PyPDFLoader(
    file_path="./data/pdf1.pdf"
)

i = 0
for doc in pdfloader.lazy_load():
    i += 1
    print(i)