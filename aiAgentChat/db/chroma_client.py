import chromadb
from chromadb.config import Settings
from utils.config_handler import db_conf
from utils.logger_handler import logger


def get_chroma_client():
    """获取 ChromaDB 客户端"""
    chroma_config = db_conf["chroma"]
    try:
        client = chromadb.HttpClient(
            host=chroma_config["host"],
            port=chroma_config["port"],
            settings=Settings(
                chroma_client_auth_provider=chroma_config["auth_provider"],
                chroma_client_auth_credentials=chroma_config["auth_credentials"]
            )
        )

        # 测试连接
        heartbeat = client.heartbeat()
        logger.info(f"ChromaDB 连接成功，心跳: {heartbeat}")

        return client
    except Exception as e:
        logger.error(f"ChromaDB 连接失败: {e}")
        raise


# 全局客户端实例
chroma_client = get_chroma_client()
