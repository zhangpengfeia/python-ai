"""
web框架对比：
1.Django
    2005年
    开箱即用，内置ORM
2.Flask
    2010年
    微内核，可扩展
3.FastAPI（主流）
    2018年出现，理论上只有一个线程，有时候会开多线程
    轻量型，高性能，现代化
==========================================
WSGI / ASGI:
python的社区规范，主要为Web服务器和Web应用程序提供统一规范
1.Web服务器：客户端请求入口
    主要负责：soket 通信，报文解析，建立http连接，处理应用程序响应结果，ASGI 负责启动事件循环uvloop，管理多线程进程
    常见ASGI服务器：uvicorn（主流）
2.Web应用程序：请求的应用程序
    主要负责：业务逻辑
    常见ASGI服务器：FastAPI（主流），Starlette
如何对接：
1.ASGI应用程序必须抛出 app 可调用对象
    app(scope, receive, send) -> CoroutineType
        scope：连接上下文信息字典，receive: 异步无参数函数，用于接收消息，send: 异步单参数函数，用于发送消息
    过程：
    1.查路由表
    2.拿到app返回结果，使用send发送响应
================================
SwaggerUI,Redoc:
OpenAPI：使用标准格式描述接口规格，所有请求工具都支持apenAPI格式，可以导入导出json。访问 /openapi.json
根据openAPI生成文档：
    SwaggerUI：交互式测试
    Redoc：只做阅读
可以通过路由字典参数修改生成的json
也可以根据环境变量禁用
FastAPI({
    docs_url=None
    redoc_url=None
    openapi_url=None
})

==========================
pydantic: 数据验证
验证数据类型错误时报错，可以做更多精细化，再openapi.json里看到
"""