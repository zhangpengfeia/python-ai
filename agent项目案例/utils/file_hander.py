import hashlib
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from agent项目案例.utils.log_tool import logger

# 获取文件的md5的十六进制字符串
def get_file_md5_hex(filepath: str): #
    if not os.path.exists(filepath):
        logger.error(f"[md5计算]文件{filepath}不存在")
        return
    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]文件{filepath}不是文件")
        return

    md5_obj = hashlib.md5()
    chunk_size = 4096
    try:
        with open(filepath, 'rb') as f:
            while chunk:= f.read(chunk_size):
                md5_obj.update(chunk)
            return md5_obj.hexdigest()
    except Exception as e:
        logger.error(f"[md5计算]文件{filepath}计算md5失败，错误信息：{e}")


def listdir_with_allowed_type(filepath: str, allowed_type: tuple[str]):
    files = []
    if not os.path.isdir(filepath):
        logger.error(f"[listdir_with_allowed_type]{filepath}不是目录")
        return allowed_type

    for file in os.listdir(filepath):
        if file.endswith(allowed_type):
            files.append(os.path.join(filepath, file))
    return tuple(files)

def pdf_loader(filepath: str, password: str = None) -> list[Document]:
    return PyPDFLoader(filepath, password).load()

def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath).load()


