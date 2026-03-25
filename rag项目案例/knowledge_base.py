import os
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
    pass
def save_md5(md5_str: str):
    # 将传入md5字符串，记录到文件内保存
    with open(config.md5_path, 'w', encoding="utf-8") as f:
        f.write(md5_str + '\n')
    pass

def get_string_md5(input_str):
    # 将传入字符串转换为md5字符串
    pass

class KnowledgeBaseService(object):
    def __init__(self):
        self.chroma = None
        self.spliter = None

    def upload_by_str(self, data, filename):
        # 将传入字符串，进行向量化
        pass