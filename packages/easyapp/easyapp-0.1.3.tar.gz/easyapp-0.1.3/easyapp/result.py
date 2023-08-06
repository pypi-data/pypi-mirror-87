from config.application_model import Option
import enum
from typing import Any, Optional
from pydantic import BaseModel
from fastapi.responses import Response

import typing
import json
from . import settings

from enum import Enum
from . import settings

# 基础错误代码定义
# class ErrCode(enum):
#     SUCCESS: 0
#     LOGIN_FAIL: 1000
#     REQUEST_VALIDATE_FAIL: 2000
#     FILE_ERROR: 3000
#     COMMON_ERROR: 8000
#     UNKNOWN_ERROR: 9000


def response2json(content: Any):
    return json.dumps(
        content,
        ensure_ascii=False,
        allow_nan=False,
        indent=None,
        separators=(",", ":"),
    ).encode("utf-8")


class MyResponse(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        r = {
            'code': 0,
            'data': content
        }
        return response2json(r)


class ResultError(BaseModel):
    code: int = 5000
    msg: str = ''  # 对外暴漏的错误信息
    detail: Any = None  # 对外暴漏的错误详细信息
    errid: str = ''  # 记录到日志中的错误id，排查问题时使用
    errmsg:Optional[Any] = None  # 不公开的错误信息，排查问题使用
    traceback: Optional[str] = None  # 堆栈信息，排查问题使用

    # def getDict(self):
    #     dic = {}
    #     dic.update('code', self.code)
    #     dic.update('msg', self.msg)
    #     dic.update('detail', self.detail)
    #     dic.update('errid', self.errid)
    #     dic.update('errmsg', self.errmsg)
    #     dic.update('traceback', self.traceback)


class MyResponseError(Response):
    media_type = "application/json"

    def render(self, content: ResultError) -> bytes:
        dic = dict(content)
        if not settings.DEBUG:
            del(dic['detail'])
            del(dic['errmsg'])
            del(dic['traceback'])

        return response2json(dic)


class MyException(Exception):
    def __init__(self, msg: str, code: int = 5000, detail: Any = None, errmsg: str = None):
        self.code = code
        self.msg = msg
        self.detail = detail
        self.errmsg = errmsg

    code: int = 5000
    msg: str
    detail: Any = ''  # 对外暴漏的错误详细信息
    # errid: str = ''     #记录到日志中的错误id，排查问题时使用
    errmsg: str = ''  # 不公开的错误信息，排查问题使用
    # traceback: str = '' #堆栈信息，排查问题使用
