#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import time
import MySQLdb
import traceback

script_name = sys.argv[0]


class MyMysql:
    def __init__(self, host='', user='', passwd='', db='', port=3306, charset='utf8', _log=''):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port
        self.charset = charset
        self._log = _log
        self.conn = None
        self._conn()

    def _conn(self):
        try:
            self.conn = MySQLdb.Connection(host=self.host, user=self.user, passwd=self.passwd, db=self.db,
                                           port=self.port, charset=self.charset)
            return True
        except MySQLdb.Error:
            err_msg = traceback.format_exc()
            warning_msg = '{0}======================={1}'.format(script_name, err_msg)
            self._log.critical(warning_msg)
            return False

    def _re_conn(self, num=28800, stime=3):
        _number = 0
        _status = True
        while _status and _number <= num:
            try:
                self.conn.ping()
                _status = False
            except MySQLdb.Error:
                if self._conn():
                    _status = False
                    break
                _number += 1
                time.sleep(stime)

    def select(self, sql=''):
        try:
            self._re_conn()
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.cursor.close()
            return result
        except MySQLdb.Error:
            err_msg = traceback.format_exc()
            warning_msg = '{0}======================={1}'.format(script_name, err_msg)
            self._log.critical(warning_msg)
            return False

    def select_one(self, sql=''):
        try:
            self._re_conn()
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            self.cursor.close()
            return result
        except MySQLdb.Error:
            err_msg = traceback.format_exc()
            warning_msg = '{0}======================={1}'.format(script_name, err_msg)
            self._log.critical(warning_msg)
            return False

    def select_limit(self, sql='', offset=0, length=20):
        sql = '%s limit %d , %d ;' % (sql, offset, length)
        return self.select(sql)

    def query(self, sql=''):
        try:
            self._re_conn()
            self.cursor = self.conn.cursor()
            self.cursor.execute("set names utf8")
            result = self.cursor.execute(sql)
            self.conn.commit()
            self.cursor.close()
            return result
        except MySQLdb.Error:
            err_msg = traceback.format_exc()
            warning_msg = '{0}======================={1}'.format(script_name, err_msg)
            self._log.critical(warning_msg)
            self.cursor.close()
            return False

    def transaction_query(self, sql=''):
        try:
            self._re_conn()
            self.cursor = self.conn.cursor()
            self.cursor.execute("set names utf8")
            result = self.cursor.execute(sql)
            return result
        except MySQLdb.Error:
            err_msg = traceback.format_exc()
            warning_msg = '{0}======================={1}'.format(script_name, err_msg)
            self._log.critical(warning_msg)
            self.conn.rollback()
            self.cursor.close()
            return False

    def do_many(self, sql='', param=None):
        if param is None:
            param = []
        try:
            self._re_conn()
            self.cursor = self.conn.cursor()
            self.cursor.execute("set names utf8")
            result = self.cursor.executemany(sql, param)
            return result
        except MySQLdb.Error:
            err_msg = traceback.format_exc()
            warning_msg = '{0}======================={1}'.format(script_name, err_msg)
            self._log.critical(warning_msg)
            self.conn.rollback()
            self.cursor.close()
            return False

    def do_commit(self):
        try:
            self._re_conn()
            self.conn.commit()
            return True
        except MySQLdb.Error:
            err_msg = traceback.format_exc()
            warning_msg = '{0}======================={1}'.format(script_name, err_msg)
            self._log.critical(warning_msg)
            return False

    def close(self):
        self.conn.close()
