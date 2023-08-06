# https://blog.csdn.net/laiyijian/article/details/80724327
# https://www.cnblogs.com/liubinsh/p/7568423.html
# https://blog.csdn.net/qq_40558166/article/details/100109288
# https://blog.csdn.net/will_awoke/article/details/8890373
# https://blog.csdn.net/kongsuhongbaby/article/details/108210895
# https://www.jianshu.com/p/d81957066ce7
# https://zhuanlan.zhihu.com/p/39928355
# https://www.cnblogs.com/xfxing/p/9322199.html
# https://blog.csdn.net/qq_40558166/article/details/100109288

# python3数据库工具类
#   https://blog.csdn.net/yang725614/article/details/99957358
#   https://cloud.tencent.com/developer/article/1439767
# pymysql之executemany()  https://blog.csdn.net/qq282881515/article/details/70638517
import pymysql
from pymysql.constants import CLIENT


class Db:

    dbconfig_default = {}

    # 连接数据库和定义游标
    def __init__(self, **dbconfig):
        if dbconfig == {}:
            dbconfig = self.dbconfig_default
        if (dbconfig == None) | (dbconfig == {}):
            raise Exception('Db.dbconfig配置参数为空')
        self.db = pymysql.connect(
            cursorclass=pymysql.cursors.DictCursor,
            client_flag=CLIENT.MULTI_STATEMENTS,
            **dbconfig)
        self.cursor = self.db.cursor()

    # 查询操作
    def select(self, sql, **pars):
        self.cursor.execute(sql)  # 执行sql语句
        result = []
        while True:
            r = self.cursor.fetchall()  # 会获取所有数据
            result.append(r)
            if not self.cursor.nextset():
                break
        if len(result) == 1:
            return result[0]
        else:
            return result

    # 增删改操作
    def change(self, sql, **pars):
        self.cursor.execute(sql)
        self.db.commit()  # 提交数据
        print('操作成功！')
        return self.cursor.rowcount  # 获取操作的行数

    # 自动关闭连接
    def __del__(self):
        self.cursor.close()
        self.db.close()


# sql = input('请输入SQl语句：')
