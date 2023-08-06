from logging import exception
import os
import traceback

from config.openapi import DOC_CONFIG
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request

from easyapp.db import Db

from . import (MyException, MyResponse, MyResponseError, ResultError, get_id,
               logger)
from .main_init import get_routers_custom, init_openapi_doc
from .tools import timeit

app = FastAPI()

app.default_response_class = MyResponse

# 开始初始化项目定制的路由
app.include_router(get_routers_custom())

# 初始化log目录
if not os.path.exists('./log'):
    os.makedirs('./log')

# 初始化文档doc参数属性
init_openapi_doc(app, DOC_CONFIG)


@app.get("/favicon.ico")
async def demo():
    return ''


@app.middleware("http")
# @timeit
async def process_authorization(request: Request, call_next):

    response = await call_next(request)
    # exception之外的其它异常，处理完后，可以返回来写入日志
    logger.bind(access=True).success(
        f"{request.method} {request.url}")
    # 如果有异常，则再打印异常日志
    # if response.
    return response

# Exception异常


@app.exception_handler(Exception)
async def exception_handler(request: Request, e: Exception):
    # logger.bind(request=request, exception=e).error('异常')
    result = ResultError(
        code=9000,
        msg='内部错误',
        detail=None,
        errmsg=str(e.args),
        errid=get_id(),
        traceback=traceback.format_exc()
    )
    # 处理完后，无法返回@app.middleware("http")，因此这里要自己写日志
    # 访问日志
    logger.bind(access=True).error(
        f"{request.method} {request.url}     {result.errid}")

    # 错误日志
    logger.error(f"1111\nHeaders:{request.headers}\n{traceback.format_exc()}")

    return MyResponseError(result)


@app.exception_handler(MyException)
async def my_exception_handler(request: Request, e: MyException):
    # logger.error(
    #     f"全局异\n{request.method}URL{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")

    result = ResultError(
        code=e.code,
        msg=e.msg,
        detail=e.detail,
        errmsg=e.errmsg,
        errid=get_id(),
        traceback=traceback.format_exc()
    )
    return MyResponseError(result)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    result = ResultError(
        code=2000,
        msg='参数或数据校验错误',
        detail=exc.errors(),
        errid=get_id(),
        errmsg=str(dict(request)),
        traceback=traceback.format_exc()
    )
    # return MyResponseError({"detail": exc.errors(), "body": exc.body})
    return MyResponseError(result)
