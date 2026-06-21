# 请求处理器：统一异常处理、响应封装
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

# 配置日志
logger = logging.getLogger(__name__)
def add_exception_handlers(app: FastAPI):
    """
    为FastAPI应用添加全局异常处理器
    """
    # 处理HTTP异常（如404、403等）
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.error(f"HTTP异常: {exc.status_code} - {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "message": exc.detail,
                "data": None
            }
        )

    # 处理请求参数校验错误
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"参数校验错误: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={
                "code": 422,
                "message": "请求参数错误",
                "data": exc.errors()
            }
        )

    # 处理所有未捕获的异常
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"未捕获异常: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "message": "服务器内部错误，请稍后重试",
                "data": None
            }
        )