"""
流式输出：
sse模式：
    本质是http请求，http长连接也可以实现流式输出，只不过sse有传输规范，content-type:text/event-stream，大家默认使用sse，方便第三方库封装
    错误信息：data: error message
    问题：
        中间件：不使用 response 处理返回sse内容
        异常处理：正常走异常处理，流式迭代中的异常自行处理，不受中间件控制
        依赖注入：所有流式内容全部完成后才会迭代完成
        token携带：原生 EventSource 只能将token放到query中，可以自定义或第三方库可以任意方式携带token
===
webSocket模式：
    全双工通信，客户端和服务器端可以同时发送数据
    1.发送http请求，约定升级为websocket协议 Connection: Upgrade，前后端保持tcp连接

    问题：
        中间件：请求/响应都不会经过http中间件
        异常处理：不会经过异常处理函数
        依赖注入：连接断开后才会迭代结束
        token携带：虽然可以放到请求头，但是浏览器不支持
                  直接放query里
                  都不携带token，连接建立过后，在发送token给服务器认证，服务器更复杂
===
sse适合 简单客服问答，文本格式，可以自动重连
webSocket适合 Agent工作流，多人在线的AI协作，文本或二进制
===
e2e ai测试：
    启动一个ai服务器，请求自己服务器，mock ai大模型返回数据
===
跑项目，大模型key
"""