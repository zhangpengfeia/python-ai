# 阿里云
from langchain_community.embeddings import DashScopeEmbeddings
# ollama
from langchain_ollama import OllamaEmbeddings
model = DashScopeEmbeddings()
model2 = OllamaEmbeddings(model="qwen3-embedding:4b")

print(model.embed_query("我喜欢你"))
print(model.embed_documents(["我喜欢你", "我稀饭你"]))