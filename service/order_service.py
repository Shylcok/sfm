#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: order_service.py
@time: 16/10/14 下午8:03
"""

from base_service import BaseService
import logging
from tornado.gen import coroutine
from tornado import gen

class OrderService(BaseService):

    def get_address(self, user_id):
        res = self.context_repos.address_repo.select_by_user_id(user_id)
        return res

    def add_address(self, user_id, address_info):
        name = address_info['name']
        mobile = address_info['mobile']
        address = address_info['address']
        is_default = address_info['is_default']
        if is_default == 1:
            self.context_repos.address_repo.update_by_user_id_set_no_default(user_id)

        res = self.context_repos.address_repo.insert(user_id, name, mobile, address, is_default)
        return {'code': 0, 'msg': '添加地址成功', 'data': res}

    def update_address(self, id, user_id, address_info):
        name = address_info['name']
        mobile = address_info['mobile']
        address = address_info['address']
        is_default = address_info['is_default']
        if is_default == 1:
            self.context_repos.address_repo.update_by_user_id_set_no_default(user_id)

        res = self.context_repos.address_repo.update_by_id(user_id, name, mobile, address, is_default, id)
        return {'code': 0, 'msg': '更新地址成功', 'data': res}

    def delete_address(self, id):
        res = self.context_repos.address_repo.delete_by_id(id)
        return {'code': 0, 'msg': '删除地址成功', 'data': res}

    def set_default(self, user_id, id):
        self.context_repos.address_repo.update_by_user_id_set_no_default(user_id)
        res = self.context_repos.address_repo.update_by_id_set_default(id)
        return {'code': 0, 'msg': '设置默认地址成功', 'data': res}

    @coroutine
    def prepare_order(self, user_id, order_type, cart_list, sku_list, counpon_code, first_pay):
        order_sku_infos = []
        order_sku_count = 0 # 商品数量
        order_sku_amount = 0 # 商品总价
        credit_amount = 0 # 额度卡透支,为负数
        ship_amount_= 0 # 运费
        pay_amount = 0 # 支付价格

        if order_type == 'cart':
            for cart_id in cart_list:
                cart_info = yield self.context_repos.cart_repo.select_by_id(cart_id)
                if cart_info is None:
                    logging.error('传入不存在的购物车id:%s' % cart_id)
                else:
                    sku_id = cart_info['sku_id']
                    sku_count = cart_info['sku_count']
                    sku_info = yield self.context_repos.expernal_repo.get_sku_info(sku_id)
                    if sku_info:
                        order_sku_count = order_sku_count + sku_count
                        sku_info['order_sku_count'] = sku_count
                        order_sku_infos.append(sku_info)
                    else:
                        logging.error('不存在的商品, sku_id=%s' % sku_id)

        elif order_type == 'sku':
            for sku in sku_list:
                sku_id = sku['sku_id']
                sku_count = sku['sku_count']
                sku_info = yield self.context_repos.expernal_repo.get_sku_info(sku_id)
                if sku_info:
                    order_sku_count = order_sku_count + sku_count
                    sku_info['order_sku_count'] = sku_count
                    order_sku_infos.append(sku_info)
                else:
                    logging.error('不存在的商品, sku_id=%s' % sku_id)


        gen.Return(order_sku_infos)


        # 计算出首付价格, 额度卡透资价格, 运费, 需要支付的价格
        # return {'sku_list': '123'}

