import os
# vector_store.py 第一行
import sys
from pathlib import Path

from utils.query_chroma import chroma_client

# 把agent_demo根目录加入搜索路径
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))


from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from model.factory import embed_model, chat_model
from utils.config_handler import chroma_conf
from utils.file_handler import txt_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.logger_handler import logger
from utils.path_tool import get_abs_path


class VectorStoreService:
    def __init__(self):
        # 向量数据库
        self.vector_store = Chroma(
            client=chroma_client,
            collection_name=chroma_conf["collection_name"],
            embedding_function=embed_model,
            persist_directory=chroma_conf["persist_directory"]
        )

        # 文本分块
        self.spliter = RecursiveCharacterTextSplitter(
            separators=chroma_conf["separators"],
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            length_function=len
        )


    # 向量数据库的检索器
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    # 数据文件内读取数据文件，转为向量存入向量库，计算 md5 去重
    def add_document(self):

        # md5 去重
        def check_md5_hex(md5_for_check):
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w", encoding="utf-8").close()
                return False # md5 没处理过
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True

        # 保存 md5
        def save_md5_hex(md5_hex_str: str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_hex_str + "\n")
        # 获取文件
        def get_file_documents(read_path: str):
            if read_path.endswith("txt"):
                return txt_loader(read_path)
            elif read_path.endswith("pdf"):
                return pdf_loader(read_path)
            return []

        allowed_files_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_type"])
        )
        # 遍历文件
        for path in allowed_files_path:
            md5_hex = get_file_md5_hex(path)
            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库] 文件{path}已处理过")
                continue
            try:
                documents = get_file_documents(path)
                if not documents:
                    logger.warning(f"[加载知识库]{path}没有有效文本，跳过")
                    continue
                split_documents: list[Document] = self.spliter.split_documents(documents)
                if not split_documents:
                    logger.warning(f"[加载知识库]{path}分片没有有效文本，跳过")
                    continue
                # 添加内容存入向量库
                self.vector_store.add_documents(split_documents)
                # 记录一键处理好的文件的 md5，避免重复加载
                save_md5_hex(md5_hex)
                logger.info(f"[加载知识库] 向量库添加文件{path}成功")
            except Exception as e:
                logger.error(f"[加载知识库] 向量库添加文件{path}失败，{str(e)}", exc_info=True)
                continue

if __name__ == '__main__':
    # 测试嵌入模型是否工作
    try:
        test_embedding = embed_model.embed_query("测试")
        logger.info(f"嵌入模型测试成功，向量维度：{len(test_embedding)}")
    except Exception as e:
        logger.error(f"嵌入模型测试失败：{str(e)}", exc_info=True)
        exit(1)
    
    vs = VectorStoreService()
    vs.add_document()
    retriever = vs.get_retriever()
    res = retriever.invoke("维护保养")
    for r in res:
        print(r.page_content)
        print("_"*20)