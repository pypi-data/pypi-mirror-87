import logging
from logging import ERROR
import os
import sys
# import time


from loguru import logger

# 先将uvicorn的日志去掉
logging.getLogger('uvicorn.access').disabled = True
logging.getLogger('uvicorn').disabled = True
logging.getLogger().disabled = True
logging.getLogger('fastapi').disabled = True


FORMAT_ACCESS = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    # "<level>{level: <8}</level> | "  #这个是要ip地址
    # "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    "<level>{message}</level>  "
)


def filter_access(record):
    return "access" in record["extra"]


logger.remove()
logger.add(sys.stderr,
           filter=filter_access,
           format=FORMAT_ACCESS
           )

def access_logger(level,request,res=None):
    if(level=="access"):
        logger.bind(access=True).success(f"{request.method} {request.url}")
    elif (level=="error"):
        logger.bind(access=True).error(f"{request.method} {request.url}")
    else:
        raise Exception('level不能是'+level)
