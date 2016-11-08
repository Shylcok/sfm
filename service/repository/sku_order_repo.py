#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: sku_order_repo.py
@time: 16/11/3 下午2:36
"""

from service.repository.base_repo import BaseRepo
from tornado.concurrent import run_on_executor


class SkuOrderRepo(BaseRepo):
    TABLE_NAME = 'sfm_sku_order'

    def insert(self, order_id, sku_id, sku_count, sku_weight, sku_amount, sku_name, sku_image_url, first_price):
        sql = """
            insert into {} set order_id=%s, sku_id=%s,sku_count=%s, sku_weight=%s, sku_amount=%s, sku_name=%s, sku_image_url=%s, first_price=%s
        """.format(self.TABLE_NAME)
        return self.db.execute_lastrowid(sql, order_id, sku_id, sku_count, sku_weight, sku_amount, sku_name,
                                         sku_image_url, first_price)

    @run_on_executor
    def select_by_order_id(self, order_id):
        sql = """
            select * from {} WHERE order_id=%s
        """.format(self.TABLE_NAME)
        return self.db.query(sql, order_id)