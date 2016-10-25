#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: cart_service.py
@time: 16/10/25 下午10:27
"""

from base_service import BaseService


class CartService(BaseService):

    def list(self, user_id):
        res = self.context_repos.cart_repo.select_by_user_id(user_id)
        return res

    def add_cart(self, user_id, sku_id, sku_count):
        res = self.context_repos.cart_repo.insert(user_id, sku_id, sku_count)
        return res

    def update_cart(self, id, sku_count):
        if sku_count == 0:
            res = self.context_repos.cart_repo.delete(id)
            return res
        else:
            res = self.context_repos.cart_repo.update(id, sku_count)
            return res

    def del_cart(self, id):
        res = self.context_repos.cart_repo.delete(id)
        return res

    def cart_count(self, user_id):
        res = self.context_repos.cart_repo.count(user_id)
        return res

