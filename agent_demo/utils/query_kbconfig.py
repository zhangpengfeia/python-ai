# 动态获取向量库
import pymysql

class KBConfig:
    def __init__(self):
        self.conn = pymysql.connect(
            host="152.136.228.231",
            user="root",
            password="123456",
            database="ai_agent",
            charset="utf8mb4"
        )

    # 获取所有知识库
    def list_all_kb(self):
        with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM kb_config")
            return cursor.fetchall()

    # 根据ID获取一个知识库（用于切换）
    def get_kb_by_id(self, kb_id):
        with self.conn.cursor(pymysql.cursor) as cursor:
            cursor.execute("""
                SELECT chroma_collection FROM kb_config WHERE id=%s
            """, (kb_id,))
            return cursor.fetchone()

# 使用示例
cfg = KBConfig()
print(cfg.list_all_kb())