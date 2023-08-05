# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Date:   2018-02-09 11:22:34
# @Last Modified by:   hang.zhang
# @Last Modified time: 2018-02-09 12:33:23

from os import kill
from DBService import MysqlService


STORE_MYSQL_HOST = "122.226.111.10"
STORE_MYSQL_USER = "funder"
STORE_MYSQL_PASSWORD = "funder"
STORE_MYSQL_PORT = 3306
STORE_MYSQL_DB = "ccb_trade_assistant"


def test_insert_null():
    """
    create table test(`name cn` varchar(20))engine innodb charset=utf8;
    """
    store_mysql_host = STORE_MYSQL_HOST
    store_mysql_user = STORE_MYSQL_USER
    store_mysql_password = STORE_MYSQL_PASSWORD
    store_mysql_port = STORE_MYSQL_PORT
    store_server = MysqlService(
        store_mysql_host, store_mysql_user, store_mysql_password, store_mysql_port)

    query_map = {"name cn": "name cn 2", "name ": "asd"}

    # print store_server.join_query_map(query_map)

    store_server.execute('insert into ccb_trade_assistant.test value("1", "None")')

def test():
    test_insert_null()

item_map = {
    "a": "b",
    "c": 1,
    "d": None,
    "e": ","
}
def test_args(item_map):
    query_str = []
    col_str = []
    for k, v in item_map.items():
        col_str.append("`%s`" % k)
        query_str.append('%%(%s)s' % k)
    col_str = ",".join(col_str)
    query_str = ",".join(query_str)
    #print(",".join(query_str))
    
    sql = "insert into table(%s) values(%s)" % (col_str, query_str)
    print(sql)
    return sql

test_args(item_map)
# cur.mogrify(ss, item_map)

if __name__ == '__main__':
    test()
