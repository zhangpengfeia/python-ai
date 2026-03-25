md5_path = "./md5.text"

collection_name="rag"
persist_directory="./chroma_db"

chunk_size = 1000 # 分割大小
chunk_overlap=100 # 分割
separators = ["\n\n", "\n", ",","。","，"] # 分割字符串

max_split_char_number = 1000 # 文本分割阈值

# 相似度检索阈值
similarity_threshold = 2

embedding_model_name = "text-embedding-v4"
chat_model_name = "qwen3:4b"