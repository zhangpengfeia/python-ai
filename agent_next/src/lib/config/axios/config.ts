/**
 * axios全局配置
 * @Author: zhangpi
 * @Date: 2023-02-09 09:42:57
 * @LastEditTime: 2025-01-01 09:38:47
 */
const config: {
  result_code: number | string;
  request_timeout: number;
  defaultbaseURL: string;
} = {
  /**
   * 接口成功返回状态码
   */
  result_code: "0000",

  /**
   * 接口请求超时时间
   */
  request_timeout: 60000 * 10,

  /**
   * 默认接口请求类型
   * 可选值: application/x-www-form-urlencoded multipart/form-data
   */
  // api前缀
  defaultbaseURL: '/v1'
};

export { config };