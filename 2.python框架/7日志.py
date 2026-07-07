"""
程序有两个接口：
stdout 标准输出接口
stdin 标准输入接口
---
请求日志：
1.使用请求中间件拦截请求，生成request_id，记录到上下文 context_var，后边每一个日志都包含request_id
2.创建请求日志对象
3.将日志对象放置到 request.state.request_log，方便其他地方获取日志对象
4.请求成功：log.success()
5.请求失败：进入 handleer 处理逻辑，改写message,500输出error日志，其他状态码输出warning日志

数据库日志：
注册SQLAchemy事件监听器，执行sql前计时，执行后创建日志对象，对于慢查询超过阈值的日志，输出warning级日志

业务日志：
通常不会全亮记录，业务日志可以统一处理也可以灵活处理，手动记录
统一处理：装饰器函数 @service_logger
"""