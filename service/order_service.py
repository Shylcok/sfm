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
from constant import *


class OrderGenerator(BaseService):
    def __init__(self):
        self.order_sku_count = 0  # 商品数量
        self.order_sku_amount = 0  # 订单商品价格 200
        self.credit_amount = 0  # 额度卡-10
        self.ship_amount = CONST_ORDER_SHIP_AMOUNT  # 运费10
        self.pay_amount = 0  # 支付价格
        self.order_sku_infos = []
        self.order_info = {}

    @coroutine
    def add_sku_list(self, sku_list):
        for sku in sku_list:
            sku_id = sku['sku_id']
            sku_count = sku['sku_count']
            first_price = sku['first_price']
            sku_info = yield self.context_repos.expernal_repo.get_sku_info(sku_id)
            if sku_info:
                sku_info['order_sku_count'] = sku_count
                sku_info['order_first_price'] = first_price
                sku_info['order_credit_price'] = int(sku_info['realPrice']) - first_price

                self.order_sku_count += sku_count
                self.order_sku_amount += sku_count * int(sku_info['realPrice'])
                self.credit_amount += sku_count * (-sku_info['order_credit_price'])
                self.pay_amount = self.order_sku_amount + self.credit_amount
                self.order_sku_infos.append(sku_info)
            else:
                logging.error('不存在的商品, sku_id=%s' % sku_id)

    @coroutine
    def add_cart_list(self, cart_list):
        for cart in cart_list:
            cart_id = int(cart['cart_id'])
            cart_info = yield self.context_repos.cart_repo.select_by_id(cart_id)
            if cart_info is None:
                logging.error('传入不存在的购物车id:%s' % cart_id)
            else:
                sku_id = cart_info['sku_id']
                sku_count = cart_info['sku_count']
                first_price = int(cart['first_price'])
                sku_info = yield self.context_repos.expernal_repo.get_sku_info(sku_id)
                if sku_info:
                    sku_info['order_sku_count'] = sku_count
                    sku_info['order_first_price'] = first_price
                    sku_info['order_credit_price'] = int(sku_info['realPrice']) - first_price

                    self.order_sku_count += sku_count
                    self.order_sku_amount += sku_count * int(sku_info['realPrice'])
                    self.credit_amount += sku_count * (-sku_info['order_credit_price'])
                    self.pay_amount = self.order_sku_amount + self.credit_amount
                    self.order_sku_infos.append(sku_info)
                else:
                    logging.error('不存在的商品, sku_id=%s' % sku_id)

    def get(self):
        self.order_info = {
            'order_sku_infos': self.order_sku_infos,
            'order_sku_count': self.order_sku_count,
            'order_sku_amount': self.order_sku_amount,
            'credit_amount': self.credit_amount,
            'ship_amount': self.ship_amount,
            'pay_amount': self.pay_amount
        }
        return self.order_info


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
    def prepare_order(self, user_id, order_type, cart_list, sku_list, counpon_code):
        # 计算出首付价格, 额度卡透资价格, 运费, 需要支付的价格
        order_info = OrderGenerator()

        if order_type == 'cart':
            yield order_info.add_cart_list(cart_list)
        elif order_type == 'sku':
            yield order_info.add_sku_list(sku_list)

        res = order_info.get()
        raise gen.Return(res)

    @coroutine
    def commit_order(self, user_id, address_id, order_type, cart_list, sku_list, user_note, coupon_code):

        # TODO: 提交订单之前锁库存
        order_info = OrderGenerator()
        if order_type == 'cart':
            yield order_info.add_cart_list(cart_list)
        elif order_type == 'sku':
            yield order_info.add_sku_list(sku_list)

        order_id = GENERATOR_ORDER_ID(user_id)

        last_rowid = self.context_repos.order_repo.insert(order_id, order_info.ship_amount,
                                                          order_info.order_sku_amount, order_info.credit_amount,
                                                          order_info.pay_amount, order_info.order_sku_count, user_id, address_id, user_note)
        if last_rowid < 0:
            # TODO: 失败解除库存
            logging.error('订单提交失败, 订单数据生成错误===》')
            logging.error(order_info.get())
            raise gen.Return({'code': 111, 'msg': '订单提交失败, 订单数据生成错误'})

        for order_sku_info in order_info.order_sku_infos:
            sku_id = order_sku_info['skuid']
            sku_count = order_sku_info['order_sku_count']
            sku_weight = order_sku_info['weight']
            sku_amount = int(order_sku_info['realPrice'])
            sku_name = order_sku_info['name']
            sku_image_url = order_sku_info['imglist'][0] if (len(order_sku_info['imglist']) > 0) else ''
            first_price = order_sku_info['order_first_price']

            self.context_repos.sku_order_repo.insert(order_id, sku_id, sku_count, sku_weight, sku_amount, sku_name,
                                                     sku_image_url, first_price)

        raise gen.Return({'code': 0, 'msg': '订单提交成功'})

    @coroutine
    def get_order_list(self, user_id):
        res = yield self.context_repos.order_repo.select_by_user_id(user_id)
        raise gen.Return(res)


