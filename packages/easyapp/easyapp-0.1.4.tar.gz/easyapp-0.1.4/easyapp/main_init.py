import os
import importlib
from sys import prefix
from fastapi import APIRouter
# from module import module_router
from fastapi.openapi.utils import get_openapi
# from . import logger
from . import logger


def get_routers_custom():
    # https://www.jianshu.com/p/885a754f88e3
    router_custom=APIRouter()
    # 找目录下文件，挨个import
    path_module = os.path.join(os.path.dirname(
        os.path.abspath("__file__")), 'module')
    
    if not os.path.exists(path_module):
        logger.warning('自定义模块初始化失败，找不到目录：'+path_module)
    else:
        list_files = os.listdir(path_module)
        for f in list_files:
            f_sp=os.path.splitext(f)
            if f_sp[-1].lower()!='.py':
                pass
            m = 'module.'+f_sp[0]            
            lib = importlib.import_module(m)
            r=getattr(lib,'router',None)
            if isinstance(r,APIRouter):
                prefix=''
                tags=[]
                router_description=getattr(r,'description')
                if router_description:
                    prefix=router_description.get('prefix','')
                    tags=router_description.get('tags',[])
                router_custom.include_router(r,prefix=prefix,tags=tags)
    return router_custom

def init_openapi_doc(app,DOC_CONFIG):
    if app.openapi_schema:
        return app.openapi_schema
    DOC_CONFIG.update({'routes': app.routes})
    openapi_schema = get_openapi(**DOC_CONFIG)
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    # return app.openapi_schema
