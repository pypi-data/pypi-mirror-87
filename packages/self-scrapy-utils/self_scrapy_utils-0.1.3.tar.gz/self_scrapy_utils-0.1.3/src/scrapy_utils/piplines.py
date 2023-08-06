#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: piplines
@time: 2020/12/7
@email: coderflying@163.com
@desc: 
"""
import traceback
import pymysql
from pymysql import IntegrityError
from twisted.enterprise import adbapi


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # 需要在setting中设置数据库配置参数
        dbparms = dict(
            host=settings['DATABASE_HOST'],
            db=settings['DATABASE_NAME'],
            port=settings['DATABASE_PORT'],
            user=settings['DATABASE_USERNAME'],
            passwd=settings['DATABASE_PASSWORD'],
            charset=settings['DATABASE_CHARSET'],
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        # 连接ConnectionPool（使用MySQLdb连接，或者pymysql）
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)  # **让参数变成可变化参数
        return cls(dbpool)  # 返回实例化对象

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addCallback(self.handle_error, item)

    def do_insert(self, cursor, item):
        tablename = item.pop('tablename')
        keys, values = list(item.keys()), list(item.values())
        keys = ['`{}`'.format(key) for key in keys]
        key_str = ','.join(keys)
        value_str = ','.join(["'{}'".format(str('' if i==None else i)) for i in values])
        sql = 'insert into {tablename}({key_str}) values({value_str})'.format(tablename=tablename, key_str=key_str, value_str=value_str)
        try:
            cursor.execute(sql)
        except Exception as e:
            if isinstance(e, IntegrityError):
                pass
            else:
                traceback.print_exc()
    def handle_error(self, failure, item):
        # 处理异步插入时的异常
        if failure:
            pass