# -*- coding: utf-8 -*-
# @Author: hang.zhang
# @Date:   2017-08-04 09:19:20
# @Last Modified by:   hang.zhang
# @Last Modified time: 2019-04-12 17:56:22

"""DB tools

"""
print("aa")
# import easylog
import sys
if sys.version_info < (3, ):
    reload(sys)
    sys.setdefaultencoding("utf-8")
    import Queue
else:
    import queue as Queue
import json
import logging
import threading
from collections import Iterable
from importlib import import_module
import threading

from bs4 import UnicodeDammit

logger = logging.getLogger(__name__)


# class DBService(threading.local):
class DBService(object):

    def __getattr__(self, key):
        # logger.debug(
        #     "menthod or attribute %s does no exists, now will be interperted call as <self.server.%s>" % (key, key))
        # return eval("super(DBService, self).server.%s" % key)
        # return eval("super(DBService, self).__getattr__('server').%s" % key)
        return eval("super(DBService, self).__getattribute__('server').%s" % key)


class RedisService(DBService):
    """this class is an improvement to the native python redis class.
    it has overwirte some function to make you use redis more convenient.

    it just overwrite the methods in native redis(but did not inherit it),
    so the methods name are keep the same, that means you don't need to adapt
    new api.
    one of the most amazing thing is, this class use `__getattr__` to bind
    unoverwritten's native redis method on  itself,

    when the method you called didn't exist
    in this class(but exists in native redis), you can also call it because at
    this time, you call will be interperted as call a Redis object.


    for example
        1. it has overwrite redis `rpush`, in this rpush, it
        will auto check the argument is list or string and if argument
        is provide as list type(iterable type), it will use redis pipe
        to transfer the command and just submit once.

        2. if the method is not overwritetn, you can also use it because
        when the method is not exists, your call will be interperted as
        call Redis object.
    """

    def __init__(self, redis_url):
        self.redis = import_module("redis")
        pool = self.redis.ConnectionPool.from_url(redis_url)
        self.server = self.redis.StrictRedis(connection_pool=pool)

    def join_pipe_commands(self, key, vals, op):
        """if given a large list or set to insert, it will auto call _pipe"""
        _pipe = self.server.pipeline()
        """warning: you must be carefull to the order !!! isinstance str must
        in the top level`if`, otherwise, insert `hello` will be interperted
        as insert [`h`,`e`,`l`,`l`,`o`]
        """
        if isinstance(vals, str) or isinstance(vals, unicode):
            eval("_pipe.%s(key, vals)" % op)
        elif isinstance(vals, Iterable):
            logger.debug("start join redis pipe...")
            for val in vals:
                eval(
                    "_pipe.%s(key, isinstance(val, dict) and json.dumps(val, ensure_ascii=False) or val)" % op)
        else:
            logger.error(
                "rpush vals %s's type is no avaliabled, type is %s" % (vals, type(vals)))
            return
        logger.debug("join redis pipe complete...start transfer to server")
        # if the return value is None indicate may occur some problems
        return _pipe.execute()

    def rpush(self, key, vals):
        return self.join_pipe_commands(key, vals, "rpush")

    def sadd(self, key, vals):
        return self.join_pipe_commands(key, vals, "sadd")


class MongoService(DBService):
    """all function args isn't bind at self, so you can directily use like this
    when you first use mongo connection ,it will bind with instance, and next time
    wher you use it, it will auto check if the instnace bind address has changed

    >>>server = MongoService()
    >>>server.find_all("mongodb://localhost:27017", "test")
    >>>server.find_all("mongodb://114.114.114.114:27017", "test")

    """

    query_thread_nums = 1

    def __init__(self, url=None, db=None):
        self.pymongo = import_module("pymongo")
        self.errors = import_module("pymongo.errors")
        if url:
            self.get_mongo_connection(url, db)

    def get_mongo_connection(self, url, db):
        # self.mongo_url & self.mongo_db to let you know your mongo location
        self.current_mongo_url = url
        self.current_mongo_db = db

        # MongoClient will auto call pymongo.uri_parser.parse_uri to check mongo url if valid
        # if invalid, function will raise InvalidURI Exception
        try:
            # 据说加上 connect=False  参数，可以解决 pymongo.errors.ServerSelectionTimeoutError 错误
            # 但是我觉得，这个是由断网引起的，估计很难吧...不知道有没有效果
            self.server = self.pymongo.MongoClient(url, connect=False)
        except self.errors.InvalidURI:
            logger.exception("mongourl <%s> is invalid..." % url)
            exit(-1)

        self.select_db(db)

    def select_db(self, db=None):
        if db:
            self.db = self.server[db]
            self.current_mongo_db = db
        else:
            # db can provide in mongo url, if mongo url have not provide
            # database, get_default_database will raise ConfigurationError
            try:
                self.db = self.server.get_default_database()
                self.current_mongo_db = db
            except self.errors.ConfigurationError:
                self.db = None

    def find_one(self, collection, query_sql, extract_fields):
        """actually the function will call function find_limit and give the limit argument as 1"""
        return self.find_limit(collection, query_sql, 1, extract_fields)

    def find_all(self, collection, query_sql, extract_fields={}, include_id=False):
        """alike the function find_one, actually call find_limit"""
        return self.find_limit(collection, query_sql, 0, extract_fields, include_id)

    def find_limit(self, collection, query_sql, limit, extract_fields={}, include_id=False):
        """alike find_one, actually call function find_limit_and_skip"""
        return self.find_limit_and_skip(collection, query_sql, limit, 0, extract_fields=extract_fields, include_id=include_id)

    def find_limit_and_skip(self, collection, query_sql, limit, skip, fetch_rate=5000, extract_fields={}, sort_fields={}, include_id=False):
        """alike find_limit, actually call function find"""
        return self.find(collection, query_sql, limit, skip, fetch_rate, extract_fields, sort_fields, include_id=include_id)

    def find(self, collection, query_sql, limit_count, skip_count=0, fetch_rate=5000, extract_fields={}, sort_fields={}, include_id=False):
        """ the <root> function when you run 'query' commands will called.
        no matter what query commands is(find_one or find_all or find_limit, etc.), actually it just the different kind
        of arguments to called this root function `find`.

        find is from pymongo.collection.find, ref: https://api.mongodb.com/python/current/api/pymongo/collection.html
        but i wanner explain what the argument `fetch_rate` is:

        when your query return a large numbers of result(like use find_all, to extract all result in a collection),
        you may wait until query done and fetch completed for a long time. during this period, you don't know
        how many querys has been done or even if query still alive(sometime the query will crashed).
        fetch_rate is the argument that control how many results to fetch in one time(default to 5k), and with the fetch_rate,
        you can directily know the query rate.
        """

        # TODO: check server or db if valid
        #
        # print collection, query_sql, limit_count, skip_count
        logger.info("in find: ")
        result_count = self.db[collection].find(
            query_sql, limit=limit_count, skip=skip_count).count(with_limit_and_skip=True)
        logger.info("count end")

        if not sort_fields:
            sort_fields = None
        else:
            tmp_sort_fields = []
            for k, v in sort_fields.items():
                if v == 1 or v == "1":
                    # print "in DBService sort v = 1 \n\n"
                    tmp_sort_fields.append((k, self.pymongo.ASCENDING))
                elif v == -1 or v == "-1":
                    tmp_sort_fields.append((k, self.pymongo.DESCENDING))
            sort_fields = tmp_sort_fields

        if not include_id:
            fields = {"_id": False}
        else:
            fields = {}
        fields.update(extract_fields)
        fields = None
        print("\n\n now fields is %s" % fields)

        rate, result_list = 0, []

        self.query_cmd_queue = Queue.Queue()
        while rate < result_count:
            # _id will cause TypeError: ObjectId('5982997934cbbaf8d033f86c') is not JSON serializable
            # and the dict extract from mongo is unicode, for example:{u'crawled_server': u'localhost'}
            # eval and json.dumps are used to convert to truly dict type

            # you should be carefull to limit 0, limit 0 means get all result
            #print "command is self.db[collection].find(query_sql, limit=%s, skip=%s, sort=%s)" % (fetch_rate if limit_count > fetch_rate or limit_count <=0 else limit_count, rate if rate > skip_count else skip_count, sort_fields)

            # from pymongo.cursor import CursorType

            # result_list.extend(list(self.db[collection].find(
            # query_sql, projection=fields, limit=fetch_rate if limit_count > fetch_rate or limit_count <=0 else limit_count, skip=rate if rate > skip_count else skip_count, sort=sort_fields)))
            current_fetch_rate =  fetch_rate if limit_count > fetch_rate or limit_count <=0 else limit_count
            current_rate = rate if rate > skip_count else skip_count
            # cmd = """self.db["%(collection)s"].find(%(query_sql)s,
            #                             projection=%(fields)s,
            #                             limit=%(current_fetch_rate)s,
            #                             skip=%(current_rate)s,
            #                             sort=%(sort_fields)s)""" % ({
            #                                     "collection": collection,
            #                                     "query_sql": query_sql,
            #                                     "fields": fields,
            #                                     "current_fetch_rate": current_fetch_rate,
            #                                     "current_rate": current_rate,
            #                                     "sort_fields": sort_fields,
            #                                 })
            cmd = """self.db["%(collection)s"].find(%(query_sql)s, projection=%(fields)s, limit=%(current_fetch_rate)s, skip=%(current_rate)s, sort=%(sort_fields)s)""" % ({
                                                "collection": collection,
                                                "query_sql": query_sql,
                                                "fields": fields,
                                                "current_fetch_rate": current_fetch_rate,
                                                "current_rate": current_rate,
                                                "sort_fields": sort_fields,
                                            })
            # print cmd
            self.query_cmd_queue.put(cmd)
            rate += fetch_rate
            logger.info("rate:result_count: [%d / %d]" % (rate, result_count))
        logger.info("combane end")
        self.result_list = []
        task_list = []
        for i in xrange(self.query_thread_nums):
            t = threading.Thread(target=self._call_query_cmd, args=("Thread-[%d]" % i, result_count, ))
            t.start()
            task_list.append(t)

        logger.info("task start end")
        logger.info("task_list len is %s" % len(task_list))
        for t in task_list:
            logger.info("task start")
            t.join()
            logger.info("task_end")
        logger.info("all down return")
        return self.result_list


    def _call_query_cmd(self, thread_name, result_count):
        # collection, query_sql, limit_count, skip_count, fetch_rate, fields, sort_fields = args
        logger.info("[%s] start _call_query_cmd" % thread_name)
        while True:
            try:
                cmd = self.query_cmd_queue.get(timeout=1)
            except Queue.Empty:
                import traceback
                traceback.print_exc()
                break
            # print "%s current run cmd %s" % (thread_name, cmd)
            # logger.info("%s current run cmd %s" % (thread_name, cmd))
            # print self.result_list
            logger.info("execute %s" % cmd)
            result = list(eval(cmd))
            logger.info("execute %s end" % cmd)
            self.result_list.extend(result)
            # print "fetch rate [%d / %d]" % (len(self.result_list), result_count)
            logger.debug("%s fetch rate [%d / %d]" % (thread_name, len(self.result_list), result_count))


    def insert(self, collection, document):
        """auto check insert many or insert_one"""
        # use insert instead of insert_many...because just insert has argument `check_keys` to avoid xxxx must not contain '.'
        if type(document) not in (list, set, tuple):
            document = [document]
        for d in document:
            self.db[collection].insert(d, check_keys=False)

    def replace_one(self, collection, query_sql, document, upsert=False):
        """mongo save(replace), has not save multi argument, replace or save can only replace one"""
        # return self.replace(collection, query_sql, document, multi=False)
        __replace = self.db[collection].replace_one(query_sql, document, upsert)
        return __replace.modified_count

    def update_one(self, collection, query_sql, document, upsert=False):
        __update = self.db[collection].update_one(query_sql, document, upsert)
        return __update.modified_count

    def delete_one(self, collection, query_sql):
        return self.delete(collection, query_sql)

    def delete_all(self, collection, query_sql):
        return self.delete_all(collection, query_sql, True)

    def delete(self, collection, query_sql, multi=False):
        """merge delete_one and delete_many by use argument multi"""
        __delete = self.db[collection].delete_one(query_sql) if not multi else self.db[
            collection].delete_many(query_sql)
        return __delete.deleted_count

    def list_all_collections(self, db=None):
        if not db or self.current_mongo_db == db:
            return self.convert_unciode_result(self.db.collection_names())
        else:
            # if db not match, change db & recall againe
            self.select_db(db)
            return self.list_all_collections(db)

    def list_all_dbs(self):
        """ convert [u"admin", u"local"] -> ["admin", "local"]"""
        return self.convert_unciode_result(self.server.database_names())

    def collection_result_count(self, collection):
        return self.db[collection].count()

    def convert_unciode_result(self, result):
        """ convert [u"admin", u"local"] -> ["admin", "local"]
        or {u"中文": u"not bad"} -> {"中文": "not bad"}
        because somethings bas will occur when the result is not in english
        """
        return eval(json.dumps(result, ensure_ascii=False))


class MysqlService(DBService):

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
        value = map(lambda x: '"%s"' % ( ( not isinstance(x[1], str) or not isinstance(x[1], unicode) ) and str(x[1]).replace("\\", "\\\\").replace('"', '\\"') or x[1].replace("\\", "\\\\").replace('"', '\\"')), dict_list)

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
        if isinstance(s, unicode):
            # return s
            s = str(s)
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
            x = str(x)
            if isinstance(x, unicode):
                value.append(x)
            else:
                print("%s encoding %s" % (x,UnicodeDammit(x).original_encoding))
                e = UnicodeDammit(x).original_encoding
                if e:
                    x = x.decode(e)
                value.append(x)
        # value = ",".join(value)
        # value_length =
        tmp_value = ['%s' for i in  xrange(len(value))]
        tmp_value = ",".join(tmp_value)
        print("\n\n\n tmp_value %s \n\n" % tmp_value)
        return sql_template % (insert_table, fields, tmp_value), value



    def __init__(self, host, user, password, port):
        self.sqlalchemy = import_module("sqlalchemy")
        self.server = self.sqlalchemy.create_engine("mysql+mysqldb://%s:%s@%s:%s/?charset=utf8&use_unicode=1" % (user, password, host, port), encoding='utf-8')

    def query(self, sql):
        query_result = self.execute(sql)
        # return query_result.fetchall()
        return [dict(i) for i in query_result]

    def execute(self, sql):
        if isinstance(sql, str) or isinstance(sql, unicode):
            result = self.server.execute(sql)

        return result

    def execute_with_argument(self, sql, argument=None):
        if isinstance(sql, str) or isinstance(sql, unicode):
            result = self.server.execute(sql, argument)

        return result

    def select_db(self, db):
        # print "use %s;" % db
        self.execute("use %s;" % db)



def test_mongo_service():
    server = MongoService("mongodb://localhost:27017/easyspider")
    print("all mongo dbs are %s" % server.list_all_dbs())
    print("db easyspider's collections are %s" % server.list_all_collections())

    # test call not exist method in MongoService, pay attention to this result,
    # original method collection_names will return like [u"admin"] not
    # ["admin"]
    print("db easyspider's collections are %s" % server.easyspider.collection_names())

    # test change db
    print("db admin's collections are %s" % server.list_all_collections("admin"))
    print("select db easyspider again", server.select_db("easyspider"))

    # test insert one
    insert_result = {"test": "hello"}
    print("insert %s " % insert_result, server.insert("test_collection", insert_result))

    # test insert many
    insert_result = [{"info2": ["1", "中文", "english"]},
                     {"info2": ["2", "中文", "english"]}]
    print("insert %s " % insert_result, server.insert("test_collection", insert_result))

    # test insert many tyep is tuple
    insert_result = ({"info2": ["1", "中文", "english"]}, {
                     "info2": ["2", "中文", "english"]})
    print("insert %s " % str(insert_result), server.insert("test_collection", insert_result))

    # test find method, find_one
    print("find one in test_collection ", server.find_one("test_collection", {}))

    # test find all
    print("find all in test_collection ", server.find_all("test_collection", {}))

    # test find last result
    collection_result_count = server.collection_result_count("test_collection")
    print("test_collection have %s result" % collection_result_count)
    print("test_collection last result is %s" % server.find_limit_and_skip("test_collection", {}, 1, collection_result_count - 1))

    # test delete one
    print("test del one %s" % server.delete("test_collection", {}))
    # count now result
    collection_result_count = server.collection_result_count("test_collection")
    print("test_collection have %s result" % collection_result_count)
    # test delete all
    print("test del all %s" % server.delete("test_collection", {}, multi=True))


def test_redis_service():
    server = RedisService("redis://127.0.0.1")
    print(server.ping())
    # test call not exists method in RedisService
    print( server.ping())

    # test rpush list
    print( server.rpush("test", [i for i in range(10)]))
    print( server.rpush("test2", ["hello", {"zhang": "yiTian"}, 3]))

    # test rpush str
    print( server.sadd("test3", "ni hao"))
    print( server.sadd("test4", ["你好", "China"]))

    # test call not exists method in RedisService
    print (server.hset("test5", "zhang", {"Tian": 1}))

    # test if need to convert unicode
    print( server.hset("test5", "中国", "no bad"))
    print( server.hgetall("test5"))
    print( server.hgetall("test5").keys()[0], server.hgetall("test5").values()[0])


def test_mysql_service():
    print( MysqlService.join_sql_from_map("test_table", {"first_name": "zhang", "last_name": "yiTian"}))
    print( MysqlService.join_sql_from_map("test_table", {"first_name": "zhang", "last_name": 'yi"Tian'}))



def test_multi_mongo_service():
    url = "mongodb://molbase:molbase@122.226.111.10:27017/"
    m = MongoService(url)
    m.select_db("drugfutureCrawler")
    m.find_all("drugfutureCrawler", {})


def main():
    # test_mongo_service()
    # test_redis_service()
    # test_mysql_service()
    test_multi_mongo_service()
if __name__ == '__main__':
    main()
