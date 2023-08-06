'''
pip制作安装包时的配置文件，详见make.bat。
每次打包前请手工修改version的值
'''
from setuptools import setup, find_packages
setup(
    name='easyapp',  # 打包后的包文件名
    version='0.1.4',
    description='a smart api framework based on fastapi',
    keywords=["api", "fastapi", "easyapp", "smart"],
    license="MIT Licence",
    author='JackWang',
    author_email='perwang@sina.com',
    url='http://www.app09.com',
    # packages=[''],
    packages=find_packages(),
    # package_dir={'..': '*'},
    # 需要安装的依赖
    install_requires=[
        'fastapi>=0.61.2',
        'uvicorn>=0.11.8',
        'PyMySQL>=0.8.0',
        'loguru>=0.5.3',
    ],
    # 此项需要，否则卸载时报windows error
    zip_safe=False
)

# https://www.cnblogs.com/maociping/p/6633948.html
# http://www.3qphp.com/index.php?a=shows&catid=29&id=125
# https://blog.csdn.net/hjxzt1/article/details/73741495
# https://blog.csdn.net/orangleliu/article/details/60958525
# https://www.cnblogs.com/Lands-ljk/p/5880483.html  子目录加上  __init__.py才能被打包进去
