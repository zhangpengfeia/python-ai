import chromadb
from chromadb.config import Settings

# 🌟 修正：host 不要写 http://，直接写 IP 或 127.0.0.1
chroma_client = chromadb.HttpClient(
    host="152.136.228.231",  # 🌟 这里去掉了 http://
    port=8100,
    settings=Settings(
        chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
        chroma_client_auth_credentials="admin"
    )
)
# 测试连接
try:
    print("✅ 连接成功，心跳:", chroma_client.heartbeat())
    collection = chroma_client.get_or_create_collection("rag_knowledge")
    print("✅ 集合操作正常:", collection.name)
except Exception as e:
    print("❌ 连接失败:", e)