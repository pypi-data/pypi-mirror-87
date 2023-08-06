# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Date:   2018-03-19 10:05:02
# @Last Modified by:   hang.zhang
# @Last Modified time: 2018-03-19 11:33:44
from DBService import MysqlService
import time

from twisted.internet.threads import deferToThread
import threading

MYSQL_HOST = "192.168.15.70"
MYSQL_USER = "root"
MYSQL_PASSWORD = "0000"
MYSQL_PORT = 3306
MYSQL_DB = "easy_admin"


sql1 = "select * from node limit 1;"
sql2 = "insert into node(name) value('asdasdasd')"


def main():
    server = MysqlService(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT)
    server.select_db(MYSQL_DB)
    # time.sleep(2)
    # result = server.query(sql)

    # time.sleep(1000)
    result = server.execute(sql2)
    print u"停止3秒再来"
    print server.query("show variables like '%%timeout';")
    # time.sleep(3)
    # result = server.execute(sql)
    raw_input(u"等待你去关掉mysql，然后再开")
    print u"开始执行"
    time.sleep(3)
    # result = server.query(sql2)
    result = server.execute(sql2)
    print result


def test_defer():
    print u"进入defer"
    d = deferToThread(error)
    d.addErrback(test_defer)
    return d


def error():
    # 发生错误
    print u"发生错误"
    raise Exception


def work_on_new_thread(fun, *args, **kwargs):
    t = threading.Thread(target=fun)
    t.setDaemon(True)
    t.start()


def loop_error():
    error_limit = 1
    while True:
        print "loop"
        time.sleep(2)
        error_limit -= 1
        if not error_limit:
            raise Exception()


def my_defer():
    try:
        work_on_new_thread(loop_error)
    except Exception:
        print "\n\n\n\nwork error !!!!!!!"
    while True:
        print "my........defer"
        time.sleep(1)


if __name__ == '__main__':
    # main()
    # test_defer()
    # while Treu
    # print u"执行完成"
    my_defer()
