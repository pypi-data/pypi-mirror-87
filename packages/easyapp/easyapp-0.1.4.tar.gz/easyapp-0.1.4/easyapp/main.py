import json
import os
import traceback
from typing import Optional

from config.openapi import DOC_CONFIG
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from pymysql.err import Error as MysqlError
from ujson import encode

from . import (MyException, MyResponse, MyResponseError, ResultError, get_id,
               logger)
from .main_init import get_routers_custom, init_openapi_doc

app = FastAPI()

app.default_response_class = MyResponse

# 开始初始化项目定制的路由
app.include_router(get_routers_custom())

# 初始化log目录
# if not os.path.exists('./log'):
#     os.makedirs('./log')

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
    # logger.bind(access=True).success(
    #     f"{request.method} {request.url}")
    # log.access_logger('error',request)
    # 如果有异常，则再打印异常日志
    # if response.
    return response


@app.exception_handler(Exception)
async def exception_handler(request: Request, e: Exception):
    '''未处理的异常拦截处理


    和后续其它异常拦截不同
        1.Exceptin无法返回@app.middleware("http")
        2.traceback会自动打印
    '''
    result = ResultError(
        code=9000,
        msg='内部错误',
        detail=None,
        errmsg=str(e.args),
        errid=get_id(),
        traceback=traceback.format_exc()
    )
    log_error('未处理的异常', request, result, False)
    return MyResponseError(result)


@app.exception_handler(MyException)
async def my_exception_handler(request: Request, e: MyException):
    '''各业务模块中抛出的通用业务异常

    '''
    result = ResultError(
        code=e.code,
        msg=e.msg,
        detail=e.detail,
        errmsg=e.errmsg,
        errid=get_id(),
        traceback=traceback.format_exc()
    )

    log_error('业务异常', request, result)
    return MyResponseError(result)


@app.exception_handler(MysqlError)
async def my_exception_handler(request: Request, e: MysqlError):
    '''mysql数据库各种异常

    '''
    result = ResultError(
        code=4000,
        msg='内部错误',
        detail='',
        errmsg=str(e.args),
        errid=get_id(),
        traceback=traceback.format_exc()
        # sql语句也要弄出来
    )

    log_error('数据库异常:'+str(type(e)), request, result)
    return MyResponseError(result)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> MyResponseError:
    '''fastapi抛出的请求参数校验异常

    '''
    result = ResultError(
        code=2000,
        msg='参数或数据校验错误',
        detail=exc.errors(),
        errid=get_id(),
        # errmsg=str(dict(request)),
        traceback=traceback.format_exc()
    )

    log_error('参数或数据校验错误', request, result)
    return MyResponseError(result)


def log_error(message: str, request: Request, result: Optional[ResultError], printtrace: bool = True):
    """全局拦截中间件的错误日志打印方法

    Args:
        message (str): 错误分类，打印在第一行
        request (Request): 请求实例信息
        result (Optional[ResultError]): 错误封装类
        printtrace (bool, optional): 是否打印traceback信息. Defaults to True.
    """

    if printtrace:  # 有些异常已经自己打印traceback了，这里就不在打印了
        logger.error(f"\n\nERROR:   {message}\n{traceback.format_exc()}")

    # result中的traceback不打印输出，格式不好看，并且前面已经输出了，这里要删掉该key
    result_dict = dict(result)
    del result_dict['traceback']

    logger.error('\nrequest:'+str(dict(request))+'')
    logger.error('\nresponse:'+json.dumps(result_dict,
                                          indent=4, ensure_ascii=False))
