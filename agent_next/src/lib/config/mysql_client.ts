import mysql from 'mysql2/promise';

const mysqlConfig = {
  host: process.env.MYSQL_HOST || 'localhost',
  port: parseInt(process.env.MYSQL_PORT || '3306'),
  user: process.env.MYSQL_USER || 'root',
  password: process.env.MYSQL_PASSWORD || '',
  database: process.env.MYSQL_DATABASE || 'ai_agent',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
};

let pool: mysql.Pool | null = null;

export async function getConnection(database?: string) {
  try {
    if (!pool) {
      const config = { ...mysqlConfig };
      if (database) {
        config.database = database;
      }
      pool = mysql.createPool(config);

      // 测试连接
      await pool.getConnection();
      console.log('MySQL 数据库连接成功');
    }
    return pool;
  } catch (err: any) {
    console.error('数据库连接失败:', err.message);
    throw new Error('数据库连接失败: ' + err.message);
  }
}

export async function closeConnection() {
  if (pool) {
    await pool.end();
    pool = null;
    console.log('MySQL 数据库连接已关闭');
  }
}
