import uuid
import pymysql
from datetime import datetime
from utils.logger_handler import logger

# MySQL 配置（跟你 vector_store 一致）
DB_CONFIG = {
    "host": "152.136.228.231",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "database": "ai_agent",
    "charset": "utf8mb4"
}


class ChatSession:
    def __init__(self):
        self.conn = pymysql.connect(**DB_CONFIG)
        self.conn.autocommit(True)

    # ==================== 会话相关 ====================
    def create_session(self, session_name="新对话") -> str:
        """创建新会话，返回 session_id"""
        session_id = uuid.uuid4().hex
        try:
            with self.conn.cursor() as cursor:
                sql = """
                INSERT INTO chat_session (session_id, session_name, create_time)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (session_id, session_name, datetime.now()))
            return session_id
        except Exception as e:
            logger.error(f"创建会话失败: {e}")
            return None

    def list_sessions(self, limit=20):
        """获取会话列表"""
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = """
                SELECT session_id, session_name, create_time, update_time
                FROM chat_session
                ORDER BY update_time DESC
                LIMIT %s
                """
                cursor.execute(sql, (limit,))
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"获取会话列表失败: {e}")
            return []

    def rename_session(self, session_id, new_name):
        """重命名会话"""
        try:
            with self.conn.cursor() as cursor:
                sql = "UPDATE chat_session SET session_name=%s WHERE session_id=%s"
                cursor.execute(sql, (new_name, session_id))
            return True
        except Exception as e:
            logger.error(f"重命名失败: {e}")
            return False

    # ==================== 聊天记录相关 ====================
    def add_message(self, session_id, role, content, use_rag=0, md5=None):
        """
        保存单条聊天记录
        role: user / assistant
        """
        try:
            with self.conn.cursor() as cursor:
                sql = """
                INSERT INTO chat_message 
                (session_id, role, content, use_rag, md5, create_time)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    session_id, role, content, use_rag, md5, datetime.now()
                ))
            return True
        except Exception as e:
            logger.error(f"保存消息失败: {e}")
            return False

    def get_history(self, session_id, limit=10):
        """获取一个会话的历史消息（用于上下文）"""
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = """
                SELECT role, content
                FROM chat_message
                WHERE session_id = %s
                ORDER BY create_time ASC
                LIMIT %s
                """
                cursor.execute(sql, (session_id, limit))
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"获取历史消息失败: {e}")
            return []

    def clear_history(self, session_id):
        """清空会话消息"""
        try:
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM chat_message WHERE session_id=%s"
                cursor.execute(sql, (session_id,))
            return True
        except Exception as e:
            logger.error(f"清空历史失败: {e}")
            return False