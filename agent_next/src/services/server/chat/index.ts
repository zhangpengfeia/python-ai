// sql层
import { getConnection } from '@/lib/config/mysql_client';

export async function getTest(body: { start_date: number; query_type: number }) {
  try {
    const pool = await getConnection('crmcounter');

    // MySQL 使用预处理语句，参数用 ? 占位
    const [rows] = await pool.execute(
      'CALL p_counter_get_poster_enterprise_certification(?, ?)',
      [body.start_date, body.query_type]
    );

    // execute 返回的是 [rows, fields]，rows 就是结果集
    return rows;
  } catch (err) {
    const errorMessage = err instanceof Error ? err.message : '未知错误';
    console.error('查询失败:', errorMessage);
    return [];
  }
}
