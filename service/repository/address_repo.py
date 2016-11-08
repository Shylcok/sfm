#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: address_repo.py
@time: 16/10/25 下午4:52
"""

import logging
from base_repo import BaseRepo
from tornado.concurrent import run_on_executor


class AddressRepo(BaseRepo):
    TABLE_NAME = 'sfm_address'

    def __init__(self):
        logging.info('init AddressRepo')

    def select_by_user_id(self, user_id):
        sql = """
            select * from {} WHERE user_id=%s ORDER BY is_default DESC
        """.format(self.TABLE_NAME)
        res = self.db.query(sql, user_id)
        return res

    @run_on_executor
    def select_by_id(self, id):
        sql = """
            select * from {} WHERE id=%s
        """.format(self.TABLE_NAME)
        res = self.db.get(sql, id)
        return res

    def insert(self, user_id, name, mobile, address, is_default):
        sql = """
            insert into {} (user_id, name, mobile, address, is_default) VALUES (%s, %s, %s, %s, %s)
        """.format(self.TABLE_NAME)
        res = self.db.execute_lastrowid(sql, user_id, name, mobile, address, is_default)
        return res

    def update_by_id(self, user_id, name, mobile, address, is_default, id):
        sql = """
            update {} set user_id=%s, name=%s, mobile=%s, address=%s, is_default=%s where id=%s
        """.format(self.TABLE_NAME)
        res = self.db.execute_rowcount(sql, user_id, name, mobile, address, is_default, id)
        return res

    def update_by_id_set_default(self, id):
        sql = """
            update {} set is_default=1 WHERE id=%s
        """.format(self.TABLE_NAME)
        res = self.db.execute_rowcount(sql, id)
        return res

    def update_by_user_id_set_no_default(self, user_id):
        sql = """
            update {} set is_default=0 where user_id=%s
        """.format(self.TABLE_NAME)
        res = self.db.execute_rowcount(sql, user_id)
        return res

    def delete_by_id(self, id):
        sql = """
            delete from {} where id=%s
        """.format(self.TABLE_NAME)
        res = self.db.execute_rowcount(sql, id)
        return res
