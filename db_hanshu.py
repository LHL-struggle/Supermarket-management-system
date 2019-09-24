# import re
# import urllib.parse
# import urllib.request
# import random
# import sys
import json
import pymysql

conf = json.load(open("db.json"))  # 配置信息

# 创建数据库类
class oneself_mysql(object):
    config = {'host': conf["db_server"], 'user': conf["db_user"], 'password': conf["db_password"], 'db': conf["db_name"], 'charset': 'utf8'}
    # 初始化函数
    def __init__(self):
        self.connection = None
        self.cursor = None

    # 单行查询结果函数
    def getone(self, sql, *args):
        try:
            self.connection = pymysql.connect(**oneself_mysql.config)
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql, args)
            return self.cursor.fetchone()
        except Exception as x:
            print(x)
        finally:
            self.close()

    # 多行查询结果函数
    def getall(self, sql, *args):
        try:
            self.connection = pymysql.connect(**oneself_mysql.config)
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql, args)
            return self.cursor.fetchall()
        except Exception as x:
            print(x)
        finally:
            self.close()

    # DML数据操作函数（增删改）
    def Execute_DML(self, sql, args):
        try:
            self.connection = pymysql.connect(**oneself_mysql.config)
            self.cursor = self.connection.cursor()
            H = self.cursor.execute(sql, args)   # 有返回值：返回的是执行此语句所影响的行数
            self.connection.commit()
            return '所影响行数为：%s' % (H)
        except Exception as x:
            self.connection.rollback()
            print(x)
        finally:
            self.close()

    def close(self):
        if self.cursor:
           self.cursor.close()
        if self.connection:
            self.connection.close()



# 校验用户名
def check_user_name(user_name):
    '''
    函数功能：校验用户名是否合法
    函数参数：
    user_name 待校验的用户名
    返回值：校验通过返回0，用户名存在返回1
    '''
    # 连接数据库，conn为Connection对象
    conn = pymysql.connect(conf["db_server"], conf["db_user"], conf["db_password"], conf["db_name"])
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            # 执行任意支持的SQL语句
            cur.execute("select name from login where name=%s", (user_name,))
            # 通过游标获取执行结果
            rows = cur.fetchone()
    finally:
        # 关闭数据库连接
        conn.close()
    if rows:
        # 用户名已存在
        return 1
    return 0

# 登录验证
def check_uname_pwd(user_name, password):
    '''
    函数功能：校验用户名和密码是否合法
    函数参数：
    user_name 待校验的用户名
    password 待校验的密码
    返回值：校验通过返回0，校验失败返回1
    '''
    # 连接数据库，conn为Connection对象
    conn = pymysql.connect(conf["db_server"], conf["db_user"], conf["db_password"], conf["db_name"])

    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            # 执行任意支持的SQL语句
            cur.execute("select name from login where name=%s and passwd=password(%s)", (user_name, password))
            # 通过游标获取执行结果
            rows = cur.fetchone()
    finally:
        # 关闭数据库连接
        conn.close()

    if rows:
        return 0
    return 1


def user_reg(uname, password):
    '''
    函数功能：将用户注册信息写入数据库
    函数描述：
    uname 用户名
    password 密码
    返回值：成功返回True，失败返回False
    '''
    # 连接数据库，conn为Connection对象
    conn = pymysql.connect(conf["db_server"], conf["db_user"], conf["db_password"], conf["db_name"])

    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            # 执行任意支持的SQL语句
            cur.execute("insert into login (name, passwd) values (%s, password(%s))", (uname, password))
            r = cur.rowcount
            conn.commit()
    finally:
        # 关闭数据库连接
        conn.close()
    return bool(r)


# 写入商品信息
def WriteInfor(data):
    '''
    :param data: 商品信息
    :return:  成功返回True，失败返回False
    '''
    # 连接数据库，conn为Connection对象
    conn = pymysql.connect(conf["db_server"], conf["db_user"], conf["db_password"], conf["db_name1"])
    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            # 执行任意支持的SQL语句
            cur.execute("insert into kucun (TradeName,ProducData,RDate,ShelfLife,Pprice,Inventory) values (%s,%s,%s,%s,%s,%s)", data)
            r = cur.rowcount
            conn.commit()
    finally:
        # 关闭数据库连接
        conn.close()
    return bool(r)