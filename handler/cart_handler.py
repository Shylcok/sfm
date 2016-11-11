#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: cart_handler.py
@time: 16/10/25 下午9:49
"""

from base_handler import *
from tornado import gen


class CartHandler(BaseHandler):
    """-------------前端用户接口----------------"""

    @handler_decorator(perm=1, types={'user_id': str, 'sku_id': str, 'sku_inc_count': int}, plain=False, async=False,
                       finished=True)
    def add_cart(self, user_id, sku_id, sku_inc_count):
        """
        添加购物车
        :param user_id:
        :param sku_id:
        :param sku_count:
        :return:
        """
        res = self.context_services.cart_service.add_cart(user_id, sku_id, sku_inc_count)
        return res

    @gen.coroutine
    @handler_decorator(perm=1, types={'user_id': str}, plain=False, async=True, finished=True)
    def cart_list(self, user_id=3):
        """
        购物车列表
        :param user_id:
        :return:
        """
        res = yield self.context_services.cart_service.list(user_id)
        raise gen.Return(res)

    @handler_decorator(perm=1, types={'user_id': str}, plain=False, async=False, finished=True)
    def cart_count(self, user_id):
        """
        购物车数量
        :param user_id:
        :return:
        """
        res = self.context_services.cart_service.cart_count(user_id)
        return res

    @handler_decorator(perm=1, types={'user_id': str, 'sku_id': str, 'sku_count': int}, plain=False, async=False, finished=True)
    def update_cart(self, user_id, sku_id, sku_count):
        """
        更新购物车
        :param sku_count:
        :param sku_id:
        :param user_id:
        :return:
        """
        res = self.context_services.cart_service.update_cart(user_id, sku_id, sku_count)
        return res

    @handler_decorator(perm=1, types={'user_id': int, 'sku_id': int}, plain=False, async=False, finished=True)
    def del_cart(self, user_id, sku_id):
        """
        删除购物车记录
        :param sku_id:
        :param user_id:
        :return:
        """
        res = self.context_services.cart_service.del_cart(user_id, sku_id)
        return res