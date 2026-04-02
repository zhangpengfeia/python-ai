import sys
from pathlib import Path
import pymysql

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
from utils.query_chroma import chroma_client

# ====================== MySQL 配置 ======================
DB_CONFIG = {
    "host": "152.136.228.231",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "database": "ai_agent",
    "charset": "utf8mb4"
}

class MySQLMD5Store:
    """MD5 存储替换为 MySQL"""
    def __init__(self):
        self.conn = pymysql.connect(**DB_CONFIG)
        self.conn.autocommit(True)

    def exists(self, md5_hex: str) -> bool:
        """检查 MD5 是否存在"""
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT 1 FROM file_md5_record WHERE md5 = %s LIMIT 1"
                cursor.execute(sql, (md5_hex,))
                return cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"MySQL 查询 MD5 失败：{e}")
            return False

    def save(self, md5_hex: str, file_name: str = None):
        """保存 MD5 到数据库"""
        try:
            with self.conn.cursor() as cursor:
                sql = """
                INSERT IGNORE INTO file_md5_record 
                (md5, file_name, create_time) 
                VALUES (%s, %s, NOW())
                """
                cursor.execute(sql, (md5_hex, file_name))
        except Exception as e:
            logger.error(f"MySQL 保存 MD5 失败：{e}")


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

        # 初始化 MySQL MD5 存储
        self.md5_store = MySQLMD5Store()

    # 向量数据库的检索器
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    # 数据文件内读取数据文件，转为向量存入向量库，计算 md5 去重
    def add_document(self):

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
            file_name = Path(path).name

            # ========== 改用 MySQL 判断 ==========
            if self.md5_store.exists(md5_hex):
                logger.info(f"[加载知识库] 文件{path}已处理过（MySQL）")
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

                # ========== 保存 MD5 到 MySQL ==========
                self.md5_store.save(md5_hex, file_name)

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
        print("_" * 20)