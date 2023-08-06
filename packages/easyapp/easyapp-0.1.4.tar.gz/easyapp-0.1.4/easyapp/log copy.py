import logging
from logging import ERROR
import os
import sys
import time

from loguru import logger

# 先将uvicorn的日志去掉
logging.getLogger('uvicorn.access').disabled = True

# basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
log_path = './log'
file_format = f'_{time.strftime("%Y-%m-%d")}.log'

ACCESS_LOG_FILE = os.path.join(log_path, f'acess'+file_format)
ERROR_LOG_FILE = os.path.join(log_path, f'error'+file_format)

FORMAT_ACCESS = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    # "<level>{level: <8}</level> | "  #这个是要ip地址
    # "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    "<level>{message}</level>  "
)


def filter_access(record):
    return "access" in record["extra"]


def filter_access_error(record):
    return ("access" in record["extra"]) and (record['level'].name == 'ERROR')


def filter_error(record):
    return ("access" not in record["extra"]) and (record['level'].name == 'ERROR')


logger.remove()
logger.add(sys.stderr,
           filter=filter_access,
           format=FORMAT_ACCESS
           )
# 还缺少
logger.add(ACCESS_LOG_FILE,
           filter=filter_access,
           format=FORMAT_ACCESS,
           rotation="00:00",
           encoding='utf8'
           )

logger.add(ERROR_LOG_FILE,
           filter=filter_access_error,
           format=FORMAT_ACCESS,
           rotation="00:00",
           encoding='utf8'
           )

logger.add(
    ERROR_LOG_FILE,
    filter=filter_error,
    rotation="00:00",
    encoding='utf8'
)
