#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: order_handler.py
@time: 16/10/12 下午5:22
"""
from handler.base_handler import BaseHandler
from core.handler_decorator import handler_decorator
from tornado.gen import coroutine
from tornado.gen import Return


class OrderHandler(BaseHandler):
    """-------------收货地址----------------"""

    @handler_decorator(perm=1, types={'user_id': str}, plain=False, async=False, finished=True)
    def get_address(self, user_id):
        """
        获取收货地址
        :param user_id:
        :return:
        """
        res = self.context_services.order_service.get_address(user_id)
        return res

    @handler_decorator(perm=1, types={'user_id': str, 'address_info': dict}, plain=False, async=False, finished=True)
    def add_address(self, user_id, address_info):
        """
        添加收货地址
        :param user_id:
        :param address_info:
        :return:
        """
        res = self.context_services.order_service.add_address(user_id, address_info)
        return res

    @handler_decorator(perm=1, types={'user_id': str, 'id': str, 'address_info': dict}, plain=False, async=False,
                       finished=True)
    def update_address(self, id, user_id, address_info):
        """
        更新收货地址
        :param id:
        :param user_id:
        :param address_info:
        :return:
        """
        res = self.context_services.order_service.update_address(id, user_id, address_info)
        return res

    @handler_decorator(perm=1, types={'id': str}, plain=False, async=False, finished=True)
    def delete_address(self, id):
        """
        删除收货地址
        :param id:
        :return:
        """
        res = self.context_services.order_service.delete_address(id)
        return res

    @handler_decorator(perm=1, types={'id': str, 'user_id': str}, plain=False, async=False, finished=True)
    def set_default(self, user_id, id):
        """
        设置默认收货地址
        :param user_id:
        :param id:
        :return:
        """
        res = self.context_services.order_service.set_default(user_id, id)
        return res

    """------------------订单操作--------------------"""

    @coroutine
    @handler_decorator(perm=1, types={'user_id': str, 'order_type': str, 'cart_list': tuple, 'sku_list': tuple,
                                      'coupon_code': str}, plain=False, async=True, finished=True)
    def prepare_order(self, user_id, order_type, cart_list, sku_list, coupon_code):
        """
        订单准备
        :param user_id:
        :param order_type: cart, sku
        :param cart_list:
        :param sku_list:
        :param coupon_code:
        :return:
        """
        res = yield self.context_services.order_service.prepare_order(user_id, order_type, cart_list, sku_list,
                                                                      coupon_code)
        raise Return(res)

    @coroutine
    @handler_decorator(perm=1, types={'user_id': str, 'address_id': str, 'order_type': str, 'cart_list': tuple,
                                      'sku_list': tuple, 'user_note': str,
                                      'coupon_code': str}, plain=False, async=True, finished=True)
    def commit_order(self, user_id, address_id, order_type, cart_list, sku_list, user_note, coupon_code):
        """
        提交订单,订单生成到数据库,到达支付页
        :param user_id:
        :param address_id:
        :param order_type: cart, sku
        :param cart_list:
        :param sku_list:
        :param user_note:
        :param ext:
        :param coupon_code:
        :return:
        """
        res = yield self.context_services.order_service.commit_order(user_id, address_id, order_type, cart_list,
                                                                     sku_list, user_note, coupon_code)
        raise Return(res)

    @coroutine
    @handler_decorator(perm=1, types={'user_id': str, 'order_id': str}, plain=False, async=True, finished=True)
    def get_order_brief_for_pay(self, user_id, order_id):
        """
        获取支付前的订单简讯
        :param user_id:
        :param order_id:
        :return:
        """
        res = yield self.context_services.order_service.get_order_brief_for_pay(user_id, order_id)
        raise Return(res)

    @coroutine
    @handler_decorator(perm=1, types={'user_id': str, 'order_id': str}, plain=False, async=True, finished=True)
    def delete_order(self, user_id, order_id):
        """
        删除订单
        :param user_id:
        :param order_id:
        :return:
        """
        res = yield self.context_services.order_service.delete_order(order_id)
        raise Return(res)

    @coroutine
    @handler_decorator(perm=1, types={'user_id': str, 'order_id': str}, plain=False, async=True, finished=True)
    def confirm_order(self, user_id, order_id):
        """
        订单确认,收获
        :param user_id:
        :param order_id:
        :return:
        """
        res = yield self.context_services.order_service.confirm_order(order_id)
        raise Return(res)

    @coroutine
    @handler_decorator(perm=1, types={'user_id': str, 'order_id': str, 'reason': str}, plain=False, async=True,
                       finished=True)
    def cancel_order(self, user_id, order_id, reason):
        """
        取消订单
        :param user_id:
        :param order_id:
        :param reason:
        :return:
        """
        res = yield self.context_services.order_service.cancel_order(order_id, reason)
        raise Return(res)

    def pay_now(self, user_id, clientip, platform, order_id, type, use_balance, address_id):
        """获取交易流水号"""

    @coroutine
    @handler_decorator(perm='', types={'user_id': str, 'order_type': str, 'page': int, 'count': int}, plain=False,
                       async=True, finished=True)
    def get_order_list(self, user_id, order_type, page, count):
        """
        获取用户订单列表
        :param count:
        :param page:
        :param order_type:
        :param user_id:
        :return:
        """
        res = yield self.context_services.order_service.get_order_list(user_id, order_type, page, count)
        raise Return(res)

    @coroutine
    @handler_decorator(perm='', types={'order_id': str}, plain=False, async=True, finished=True)
    def get_order(self, order_id):
        """
        获取订单详情
        :param order_id:
        :return:
        """
        res = yield self.context_services.order_service.get_order(order_id)
        raise Return(res)

    @coroutine
    @handler_decorator(perm=1, types={'client_ip': str, 'user_id': str, 'pay_params': dict}, plain=False, async=True,
                       finished=True)
    def pay(self, client_ip, pay_params, user_id):
        """
        订单支付
        :param user_id:
        :param client_ip:
        :param pay_params:
        :return:
        """
        res = yield self.context_services.pay_sevice.pay(client_ip, user_id, pay_params)
        raise Return(res)

    @handler_decorator(perm=0, types={'orderno': str}, plain=False, async=False, finished=True)
    def apply_refund(self, orderno):
        """
        申请退款
        :param orderno:
        :return:
        """
        pass

    """---------------后台接口---------------------"""

    """
    退款,管理员操作接口
    """

    def refund(self, client_ip, refund_params):
        self.context_services.pay_sevice.refund(refund_params)

    @coroutine
    @handler_decorator(perm='', types={'user_id': str, 'order_id': str, 'logistics_id': str}, plain=False, async=True, finished=True)
    def send_out(self, user_id, order_id, logistics_id):
        res = yield self.context_services.order_service.send_out(user_id, order_id, logistics_id)
        raise Return(res)





