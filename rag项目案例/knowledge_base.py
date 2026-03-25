import hashlib
import os
from datetime import datetime

from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config_data as config

# 知识库
def check_md5(md5_str: str):
    # 检查传入md5字符串是否已经被处理
    if not os.path.exists(config.md5_path):
        # if进入表示文件不存在，那肯定没有处理过这个md5
        open(config.md5_path, 'w', encoding="utf-8").close()
        return False
    else:
        for line in open(config.md5_path, 'r', encoding="utf-8").readlines():
            line = line.strip()
            if line == md5_str:
                return True
            
def save_md5(md5_str: str):
    # 将传入md5字符串，记录到文件内保存
    with open(config.md5_path, 'w', encoding="utf-8") as f:
        f.write(md5_str + '\n')
    pass

def get_string_md5(input_str):
    # 将传入字符串转换为md5字符串
    str_bytes = input_str.encode('utf-8')
    md5_obj = hashlib.md5()
    md5_obj.update(str_bytes)
    md5_hex = md5_obj.hexdigest()
    return md5_hex

class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name, # 数据库表名
            embedding_function=DashScopeEmbeddings(), # DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory,
        ) # 向量存储的实例 chroma向量库对象
        self.spliter = RecursiveCharacterTextSplitter(
            separators=config.separators,
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            length_function=len
        ) # 文本分割器的对象
    def upload_by_str(self, data, filename):
        # 将传入字符串，进行向量化
        md5_hex = get_string_md5(data)
        if (check_md5(md5_hex)):
            return "[跳过]内容已经存在知识库中"
        if len(data) > config.max_split_char_number:
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]
        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "小白"
        }
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )
        save_md5(md5_hex)
        return "[成功]内容已经成功载入向量库"
