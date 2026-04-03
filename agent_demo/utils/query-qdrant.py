from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# 连接 Qdrant
client = QdrantClient(
    url="http://152.136.228.231:6333",
    api_key="admin",
    prefer_grpc=False,
)

# ======================
# 测试连接
# ======================
print("测试连接...")
try:
    client.get_collections()
    print("✅ Qdrant 连接成功！")
except Exception as e:
    print("❌ 连接失败：", e)
    exit()

# ======================
# 创建集合
# ======================
collection_name = "test_collection"
if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=4, distance=Distance.COSINE),
    )
    print("✅ 集合创建成功")
else:
    print("✅ 集合已存在，跳过创建")

# ======================
# 插入向量
# ======================
points = [
    PointStruct(id=1, vector=[0.1, 0.2, 0.3, 0.4], payload={"text": "测试数据1"}),
    PointStruct(id=2, vector=[0.5, 0.6, 0.7, 0.8], payload={"text": "测试数据2"}),
]

client.upsert(
    collection_name=collection_name,
    points=points
)

print("✅ 插入成功")

# ======================
# ✅ 已修复！！！
# ======================
result = client.query_points(
    collection_name=collection_name,
    query=[0.1, 0.2, 0.3, 0.4],  # 👈 这里改成 query 就好了！！！
    limit=2
)

print("\n搜索结果：")
print(result)