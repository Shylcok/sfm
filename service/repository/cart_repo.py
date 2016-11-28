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
from tornado.concurrent import run_on_executor

class CartRepo(BaseRepo):
    TABLE_NAME = 'sfm_cart'

    def __init__(self, *args):
        logging.info('init CartRepo')
        super(CartRepo, self).__init__(CartRepo)

    def select_by_user_id(self, user_id):
        sql = """
            select * from {} WHERE user_id=%s ORDER BY time desc
        """.format(self.TABLE_NAME)
        res = self.db.query(sql, user_id)
        return res

    def select_by_user_id_sku_id(self, user_id, sku_id):
        sql = """
            select * from {} WHERE user_id=%s and sku_id=%s;
        """.format(self.TABLE_NAME)
        res = self.db.get(sql, user_id, sku_id)
        return res

    @run_on_executor
    def select_by_id(self, id):
        sql = """
            select * from {} WHERE id=%s;
        """.format(self.TABLE_NAME)
        res = self.db.get(sql, id)
        return res

    def insert(self, user_id, sku_id, sku_count):
        sql = """
            insert into {} (user_id, sku_id, sku_count, time) VALUES (%s, %s, %s, %s)
        """.format(self.TABLE_NAME)
        res = self.db.execute_rowcount(sql, user_id, sku_id, sku_count, time.time())
        return res

    def update(self, user_id, sku_id, sku_count):
        sql = """
            update {} set sku_count=%s WHERE user_id=%s and sku_id=%s
        """.format(self.TABLE_NAME)
        res = self.db.execute_rowcount(sql, sku_count, user_id, sku_id)
        return res

    def update_first_price(self, user_id, sku_id, first_price):
        sql = """
            update {} set first_price=%s WHERE user_id=%s and sku_id=%s
        """.format(self.TABLE_NAME)
        res = self.db.execute_rowcount(sql, first_price, user_id, sku_id)
        return res

    def delete(self, user_id, sku_id):
        sql = """
            delete from {} WHERE user_id=%s and sku_id=%s
        """.format(self.TABLE_NAME)
        res = self.db.execute_rowcount(sql, user_id, sku_id)
        return res

    def delete_by_cart_id(self, cart_id):
        sql = """
            delete from {} WHERE id=%s
        """.format(self.TABLE_NAME)
        res = self.db.execute_rowcount(sql, cart_id)
        return res

    def count(self, user_id):
        sql = """
            select sum(sku_count) as sum from {} WHERE user_id=%s
        """.format(self.TABLE_NAME)
        res = self.db.get(sql, user_id)['sum']
        if res is None:
            return 0
        return int(res.real)
