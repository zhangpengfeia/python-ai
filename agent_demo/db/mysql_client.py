import pymysql
from utils.config_handler import db_conf
from utils.logger_handler import logger


def get_mysql_connection():
    """获取 MySQL 连接"""
    mysql_config = db_conf["mysql"]
    try:
        # 确保密码是字符串类型，去除可能的引号
        password = str(mysql_config["password"]).strip('"').strip("'")
        
        conn = pymysql.connect(
            host=str(mysql_config["host"]),
            port=int(mysql_config["port"]),
            user=str(mysql_config["user"]),
            password=password,
            database=str(mysql_config["database"]),
            charset=str(mysql_config["charset"]),
            autocommit=mysql_config.get("autocommit", True)
        )
        logger.info("MySQL 连接成功")
        return conn
    except Exception as e:
        logger.error(f"MySQL 连接失败: {e}")
        logger.error(f"配置信息 - Host: {mysql_config.get('host')}, User: {mysql_config.get('user')}, Port: {mysql_config.get('port')}")
        raise
