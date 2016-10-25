#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: cart_repo.py
@time: 16/10/25 下午11:00
"""

from service.repository.base_repo import BaseRepo
import logging
import time


class CartRepo(BaseRepo):
    TABLE_NAME = 'sfm_cart'

    def __init__(self):
        logging.info('init CartRepo')

    def select_by_user_id(self, user_id):
        sql = """
            select * from {} WHERE user_id=%s
        """
        res = self.db.query(sql, user_id)
        return res

    def insert(self, user_id, sku_id, sku_count):
        sql = """
            insert into {} (user_id, sku_id, sku_count, time) VALUES (%s, %s, %s, %s)
        """.format(self.TABLE_NAME)
        res = self.db.execute_rowcount(sql, user_id, sku_id, sku_count, time.time())
        return res

    def update(self, id, sku_count):
        sql = """
            update {} set sku_count=%s WHERE id=%s
        """.format(self.TABLE_NAME)
        res = self.db.execute_rowcount(sql, sku_count, id)
        return res

    def delete(self, id):
        sql = """
            delete from {} WHERE id=%s``
        """.format(self.TABLE_NAME)
        res = self.db.execute_rowcount(sql, id)
        return res

    def count(self, user_id):
        sql = """
            select * from {} WHERE user_id=%s
        """.format(self.TABLE_NAME)
        res = self.db.execute_rowcount(sql, user_id)
        return res