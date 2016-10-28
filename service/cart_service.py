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

    def add_cart(self, user_id, sku_id, sku_inc_count):
        cart_sku_info = self.context_repos.cart_repo.select_by_user_id_sku_id(user_id, sku_id)
        if cart_sku_info is not None:
            res = self.update_cart(user_id, sku_id, sku_inc_count + int(cart_sku_info['sku_count']))
            return res
        else:
            res = self.context_repos.cart_repo.insert(user_id, sku_id, sku_inc_count)
            return res

    def update_cart(self, user_id, sku_id, sku_count):
        if sku_count == 0:
            res = self.context_repos.cart_repo.delete(user_id, sku_id)
            return res
        else:
            res = self.context_repos.cart_repo.update(user_id, sku_id, sku_count)
            return res

    def del_cart(self, user_id, sku_id):
        res = self.context_repos.cart_repo.delete(user_id, sku_id)
        return res

    def cart_count(self, user_id):
        res = self.context_repos.cart_repo.count(user_id)
        return {'sku_count': res}

