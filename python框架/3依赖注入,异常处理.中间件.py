"""
依赖注入了解
IOC，DI,IOC容器
IOC: Inversion of Control,控制反转
DI：Dependency Injection,依赖注入

"""


"""
异常类型：
1.日志处理
2.统一的响应处理
3.自定义异常
4.pydantic异常
服务端信息不能暴露给响应
code: 状态码
message: 信息
data: 数据


异常处理：
1.主动抛出异常，HTTPException，Exception，系统自动异常等
"""

"""
中间件：安全控制，权限认证，cors，核心业务逻辑，日志记录等
横切关注点
AOP: 应该将哪些跨域多个功能，可被横切的功能，提取出来，形成一个独立的模块，称为切面

使用：app.middleware("http")(middlewareFun)
http：匹配协议是http还是websocket
请求 -》 执行第一个中间件函数（在第一个中间件函数里控制是否调用下一个中间件） -》 拿到函数响应结果作为响应
def middlewareFun(request: Request, call_next):
    response = call_next(request)
    return response
    
"""