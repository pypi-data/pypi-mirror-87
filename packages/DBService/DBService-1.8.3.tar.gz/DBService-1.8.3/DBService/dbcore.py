# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Date:   2020年10月27日15:59:27
# @Last Modified by:   hang.zhang
# @Last Modified time: 2020年10月27日15:59:31

import pdb
import sys
import traceback
import pymysql
from bs4 import UnicodeDammit
from importlib import import_module

class DBService(object):

    def __getattr__(self, key):
        # logger.debug(
        #     "menthod or attribute %s does no exists, now will be interperted call as <self.server.%s>" % (key, key))
        # return eval("super(DBService, self).server.%s" % key)
        # return eval("super(DBService, self).__getattr__('server').%s" % key)
        return eval("super(DBService, self).__getattribute__('server').%s" % key)


class MysqlService(DBService):
    def __init__(self, host, user, password, port):
        if type(port) == str:
            port = int(port)
        from dbutils.pooled_db import PooledDB
        # self.server = pymysql.connect(host=host,
        #                             user=user,
        #                             password=password,
        #                             port=port,
        #                             charset='utf8mb4',
        #                             cursorclass=pymysql.cursors.DictCursor)


        self.server = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=3,
            # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,
            # ping MySQL服务端，检查是否服务可用，如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            host=host,
            port=port,
            user=user,
            password=password,
            cursorclass=pymysql.cursors.DictCursor
            # database="数据库名",
        )
    def query(self, sql):
        s =  self.server.connection()
        with s.cursor() as cursor:
            count = cursor.execute(sql)
            return cursor.fetchall()
    def execute(self, sql):
        s =  self.server.connection()
        with s.cursor() as cursor:
            count = cursor.execute(sql)
            s.commit()
            # print("\n\nexecute %s  %s\n\n" % (sql, count))
            return count
    def select_db(self, db):
        # s =  self.server.connection()
        # s.cursor().select_db(db)
        pass

    @classmethod
    def join_sql_from_map(cls, insert_table, args_map, db_name=None):
        """ magic method, surprise method, a very helpful method to
        allow you generate insert sql script from a dict.

        e.g:
        >>>MysqlService.join_sql_from_map("test_table", {"first_name": "zhang", "last_name": "yiTian"})
        >>>'insert into test_table(`first_name`,`last_name`) value("zhang","yiTian");'

        >>>MysqlService.join_sql_from_map("test_table", {"first_name": "zhang", "last_name": 'yi"Tian'})
        >>>'insert into test_table(`first_name`,`last_name`) value("zhang","yi\"Tian");'

        with the help of this method, you no longer warry about how to generate a sql script.
        """

        sql_template = "insert into %s(%s) value(%s);"
        # dict has no order, so you should get all dict content in one time.
        dict_list = args_map.items()

        fields = ",".join(map(lambda x: "`%s`" % x[0], dict_list))
        # value = ",".join(map(lambda x: '"%s"' %
        #                         isinstance(x[1], int) and str(x[1]) or x[1].replace('"', '\\"'), dict_list))
        # value = map(lambda x: '"%s"' % ( (isinstance(x[1], int) or isinstance(x[1], float)) and str(x[1]) or x[1].replace("\\", "\\\\").replace('"', '\\"')), dict_list)
        # sometime x maybe tuple or other unbelievable type
        if sys.version_info < (3, ):
            value = map(lambda x: '"%s"' % ( ( not isinstance(x[1], str) or not isinstance(x[1], unicode) ) and str(x[1]).replace("\\", "\\\\").replace('"', '\\"') or x[1].replace("\\", "\\\\").replace('"', '\\"')), dict_list)
        else:
            # value = map(lambda x: '"%s"' % ( ( not isinstance(x[1], str) or not isinstance(x[1], bytes) ) and x[1].decode(UnicodeDammit(x[1]).original_encoding or "utf-8").replace("\\", "\\\\").replace('"', '\\"') or x[1].replace("\\", "\\\\").replace('"', '\\"')), dict_list)
            # 实在是不知道当时自己是怎么写出来这个map的，现在 总是过不了，干脆展开来重新写。。。汗颜
            # value = []
            # for k, v in dict_list:
            #     if isinstance(v, bytes):
            #         # v = v.decode(UnicodeDammit(v).original_encoding or "utf-8")
            #         pass
            #     if isinstance(v, str):
            #         v = v.replace("\\", "\\\\").replace('"', '\\"')
            #     if not v:                    
            #         value.append('null')
            #     else:
            #         value.append('"%s"' % v)
            value = map(lambda x: '"%s"' % ( ( not isinstance(x[1], str) or not isinstance(x[1], bytes) ) and str(x[1]).replace("\\", "\\\\").replace('"', '\\"') or x[1].replace("\\", "\\\\").replace('"', '\\"')), dict_list)
                

        value = ",".join(value)
        if not db_name:
            return sql_template % (insert_table, fields, value)
        sql = sql_template % ("%s.%s" % (db_name, insert_table), fields, value)
        sql = sql.replace('"None"', "null")
        return sql

    @classmethod
    def update_sql_from_map(cls, table_name, update_target, update_dict, db_name=None):
        if not db_name:
            header = "update %s set " % table_name
        else:
            header = "update %s.%s set " % (db_name, table_name)
        content, footer = [], []
        for k, v in update_dict.items():
            content.append('`%s`="%s"' % (k, str(v).replace("\\", "\\\\").replace('"', '\\"')))
        for k, v in update_target.items():
            footer.append('`%s`="%s"' % (k, str(v).replace("\\", "\\\\").replace('"', '\\"')))
        # 处理None的情况
        _content = ",".join(content).replace('"None"', "null")
        _footer = "and".join(footer).replace('"None"', "null")
        return "%s%s where %s" % (header, _content, _footer)

    @classmethod
    def join_query_map(self, query_map, item_join_symbol="=", multi_join_symbol=" and "):
        """返回 a=b, c=d... 方便用来
        1. 查询: select xxx from table where `a`="b" and `c`="d" and `e`="f";
        2. 更新: update xxx from table set `a`="b", `c`="d", `e`="f" where `a`="b" and `c`="d" and `e`="f"
        如果是要用在 select 上，自然就是 and，如果是要用在 update上，那么自然就是 " , " 分割

        之所以加上 `` 和 "" 字段，是为了防止： `name cn` = "chinese name" 这样带有空格情况，避免被分开
        另外这样操作的话，None 需要注意一下，就会有问题，需要额外处理，比如说 `name cn` = "None" 这样插入的就不是NULL 而是变成了字符串
        """
        # return multi_join_symbol.join(map(lambda item: '`%s`%s%s' % (self.mysql_escape(item[0]), item_join_symbol, item[1] and '"%s"' % self.mysql_escape(item[1]) or "null"), query_map.items())).replace("=null", " is null")
        return multi_join_symbol.join(map(lambda item: '`%s`%s%s' % (self.mysql_escape(item[0]), item_join_symbol, '"%s"' % self.mysql_escape(item[1]) if self.mysql_escape(item[1]) is not None else "null"), query_map.items())).replace("=null", " is null")

    @classmethod
    def mysql_escape(self, s):
        # 这里注释掉，遇到 b' 估计会有大问题
        if sys.version_info < (3, ):
            if isinstance(s, bytes):
                # return s
                s = str(s)
        else:
            if isinstance(s, bytes):
                # return s
                s = s.decode(UnicodeDammit(s).original_encoding) or "utf-8"
        return s.replace("\\", "\\\\").replace('"', '\\"').replace("%", "%%") if isinstance(s, str) else s


    @classmethod
    def join_sql_from_map_with_s(cls, insert_table, args_map):
        """ magic method, surprise method, a very helpful method to
        allow you generate insert sql script from a dict.

        e.g:
        >>>MysqlService.join_sql_from_map("test_table", {"first_name": "zhang", "last_name": "yiTian"})
        >>>'insert into test_table(`first_name`,`last_name`) value("zhang","yiTian");'

        >>>MysqlService.join_sql_from_map("test_table", {"first_name": "zhang", "last_name": 'yi"Tian'})
        >>>'insert into test_table(`first_name`,`last_name`) value("zhang","yi\"Tian");'

        with the help of this method, you no longer warry about how to generate a sql script.
        """

        sql_template = "insert into %s(%s) value(%s);"
        # dict has no order, so you should get all dict content in one time.
        dict_list = args_map.items()

        fields = ",".join(map(lambda x: "`%s`" % x[0], dict_list))
        # value = ",".join(map(lambda x: '"%s"' %
        #                         isinstance(x[1], int) and str(x[1]) or x[1].replace('"', '\\"'), dict_list))
        # value = map(lambda x: '"%s"' % ( (isinstance(x[1], int) or isinstance(x[1], float)) and str(x[1]) or x[1].replace("\\", "\\\\").replace('"', '\\"')), dict_list)
        # sometime x maybe tuple or other unbelievable type
        # value = map(lambda x: str(x[1]).decode("gbk"), dict_list)
        value = []
        for item in dict_list:
            x = item[1]
            if sys.version_info < (3, ):
                x = str(x)
                if isinstance(x, unicode):
                    value.append(x)
                else:
                    print("%s encoding %s" % (x,UnicodeDammit(x).original_encoding))
                    e = UnicodeDammit(x).original_encoding
                    if e:
                        x = x.decode(e)
                    value.append(x)
            else:
                if isinstance(x, bytes):
                    x = x.decode(UnicodeDammit(x).original_encoding or "utf-8")
                value.append(x)
        # value = ",".join(value)
        # value_length =
        tmp_value = ['%s' for i in  xrange(len(value))]
        tmp_value = ",".join(tmp_value)
        print("\n\n\n tmp_value %s \n\n" % tmp_value)
        return sql_template % (insert_table, fields, tmp_value), value


class RedisService(DBService):
    def __init__(self, redis_url):
        self.redis = import_module("redis")
        pool = self.redis.ConnectionPool.from_url(redis_url)
        self.server = self.redis.StrictRedis(connection_pool=pool)
        