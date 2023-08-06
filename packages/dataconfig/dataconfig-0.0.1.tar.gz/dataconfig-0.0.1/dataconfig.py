#!/usr/bin/env python
# -*- coding: utf-8 -*-


import redis
import logging
import pymysql
from utils import Mysql
from configparser import ConfigParser

################################################


class DataConfig():

    ''' 用于维护系统数据的常用工具 '''
    # 这里尽量直接操作数据, 避免调用封装的接口, 以免引入线上程序的buger

    def __init__(self, config):

        # 解析配置文件
        self.__parser_config__(config)
        self.path_config = config  # 记录配置文件的位置
        self.mysqlDb_read = {}

        # 使用默认日志
        self.logger = logging

    def __parser_config__(self, config):
        self.__ConfigParser = ConfigParser()
        self.__ConfigParser.read(config)
        pass

    def __get_config__(self, category, name):
        return self.__ConfigParser.get(category, name)

    def __get_items__(self, category):
        return self.__ConfigParser.items(category)

    def __init_redis__(self, db_name):
        self.redisDb = redis.Redis(
            host=self.__ConfigParser.get(db_name, 'host'),
            port=self.__ConfigParser.get(db_name, 'port'),
            password=self.__ConfigParser.get(db_name, 'passwd'),
            db=0,
            encoding='utf-8',
        )
        self.logger.info("init redis ok.")
        pass

    def __init_read_db__(self, db_name):

        self.mysqlDb_read[db_name] = Mysql(
            host=self.__ConfigParser.get(db_name, 'host'),
            user=self.__ConfigParser.get(db_name, 'user'),
            password=self.__ConfigParser.get(db_name, 'passwd'),
            db=self.__ConfigParser.get(db_name, 'database'),
            time_zone="+8:00",
        )
        self.mysqlDb_read[db_name].execute("set names utf8")
        self.mysqlDb_read[db_name].execute("SET SESSION group_concat_max_len=102400")

        self.logger.info("connect read_database ok.")

    def __init_mysql_conn__(self, db_name):
        sp = self.__ConfigParser.get(db_name, 'host') .split(':')
        host, port = sp[0], 3306 if len(sp) < 2 else int(sp[1])
        conn = pymysql.connect(host=host, port=port, charset='utf8',
                               user=self.__ConfigParser.get(db_name, 'user'),
                               passwd=self.__ConfigParser.get(db_name, 'passwd'),
                               )
        conn.select_db(self.__ConfigParser.get(db_name, 'database'))
        conn.autocommit(True)
        return conn

    def transaction(self, db_name):
        """
        Torndb不支持事务，这里的__enter__返回MySQLdb的cursor对象
        用法：
        try:
            with DataConnection().transaction(db_name) as cursor:
                # do sql using cursor
        except:
            # roll back后的处理逻辑
        """
        class Transaction(object):
            def __init__(self, connection):
                self.conn = connection
                self.conn._conn.autocommit(False)
                self.cursor = self.conn._conn.cursor(pymysql.cursors.SSCursor)

            def __enter__(self):
                return self.cursor

            def __exit__(self, exc_type, exc_value, exc_traceback):
                if exc_traceback is None:
                    # 正常结束
                    self.conn._conn.commit()
                else:
                    # 出错需要rollback
                    self.conn._conn.rollback()
                self.cursor.close()

        # 因为要改autocommit，用完后还会close，所以这里需要新建一个连接，事务用完后会关掉
        connection = Mysql(
            host=self.__ConfigParser.get(db_name, 'host'),
            user=self.__ConfigParser.get(db_name, 'user'),
            password=self.__ConfigParser.get(db_name, 'passwd'),
            db=self.__ConfigParser.get(db_name, 'database'),
            time_zone="+8:00",
        )
        connection.execute("set names utf8")
        connection.execute("SET SESSION group_concat_max_len=102400")
        return Transaction(connection)
