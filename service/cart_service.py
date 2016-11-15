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
import tornado.httpclient
from settings import CONFIG
import json
import tornado.gen
import tornado
from tornado.concurrent import run_on_executor
from utility.urlRequest import UrlRequest
import logging


class CartService(BaseService):

    def __init__(self, services):
        super(CartService, self).__init__(services)

    @tornado.gen.coroutine
    def list(self, user_id):
        cart_lists = self.context_repos.cart_repo.select_by_user_id(user_id)
        for cart in cart_lists:
            sku_id = cart['sku_id']
            sku_info = yield self.context_repos.expernal_repo.get_sku_info(sku_id)
            if sku_info:
                cart['sku_info'] = sku_info
            else:
                logging.error(u'不存在的商品sku_id=%s' % sku_id)

        raise tornado.gen.Return(cart_lists)

    # @run_on_executor
    # def list(self, user_id):
    #     cart_lists = self.context_repos.cart_repo.select_by_user_id(user_id)
    #     for cart in cart_lists:
    #         logging.info('sku_url:' + CONFIG['sku_url'] + cart['sku_id'])
    #         response = UrlRequest().get(CONFIG['sku_url'] + cart['sku_id'])
    #         body_dic = json.loads(response.body)
    #         cart['sku_info'] = body_dic
    #
    #     return cart_lists

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

    def del_cart(self, user_id, sku_ids):
        for sku_id in sku_ids:
            res = self.context_repos.cart_repo.delete(user_id, sku_id)
        return {'code': 0, 'msg': '删除成功'}

    def cart_count(self, user_id):
        res = self.context_repos.cart_repo.count(user_id)
        return {'sku_count': res}

