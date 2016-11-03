#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: order_repo.py
@time: 16/11/3 上午11:50
"""

from service.repository.base_repo import BaseRepo
import time
from constant import *
from tornado.concurrent import run_on_executor


class OrderRepo(BaseRepo):
    TABLE_NAME = 'sfm_order'

    def insert(self, order_id, ship_amount, sku_amount, credit_amount, pay_amount, sku_count, user_id, address_id, user_note):
        sql = """
            insert into {} set order_id=%s, state=0, ctime=%s, utime=%s, overtime=%s,
            ship_amount=%s, sku_amount=%s, credit_amount=%s, pay_amount=%s, user_id=%s, address_id=%s, status=1, user_note=%s
        """.format(self.TABLE_NAME)
        lastrowid = self.db.execute_lastrowid(sql, order_id, time.time(), time.time(),
                                         time.time() + CONST_ORDER_OVER_DURATION,
                                         ship_amount, sku_amount, credit_amount, pay_amount, user_id, address_id, user_note)
        return lastrowid

    @run_on_executor
    def select_by_user_id(self, user_id):
        sql = """
            select * from {} where user_id=%s
        """.format(self.TABLE_NAME)
        res = self.db.query(sql, user_id)
        return res