from .db import Db as __Db__
# from .log import logger
from config.application import settings
# import config.application_model
from .result import MyResponse, MyResponseError, ResultError, MyException
from .tools import IdWorker
import logging

logger=logging.getLogger()

settings = settings

# 初始化数据库默认链接
__Db__.dbconfig_default = dict(settings.DB_OPTION)

db = __Db__()  # 默认链接配置的Db实例

# logger = logger

# MyResponseError: MyResponseError = MyResponseError
# ResultError: ResultError = ResultError
# MyResponse: MyResponse = MyResponse
# MyException: MyException = MyException
get_id = IdWorker(1, 1, 1).get_id





# Python杂谈: __init__.py的作用  https://www.cnblogs.com/tp1226/p/8453854.html