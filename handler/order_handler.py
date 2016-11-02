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

    @handler_decorator(perm='', types={'user_id': str, 'order_type': str, 'cart_list': tuple, 'sku_list': tuple,
                                       'counpon_code': str}, plain=False, async=False, finished=True)
    def prepare_order(self, user_id, order_type, cart_list, sku_list, counpon_code):
        """
        订单准备
        :param user_id:
        :param order_type: cart, sku
        :param cart_list:
        :param sku_list:
        :param counpon_code:
        :return:
        """
        res = self.context_services.order_service.prepare_order(user_id, order_type, cart_list, sku_list, counpon_code)
        return res

    def commit_order(self, user_id, use_balance, address_id, cart_type, pay_type, cart_list, sku_list, user_note, ext,
                     coupon_code):
        """
        提交订单,订单生成到数据库,到达支付页
        :param user_id:
        :param use_balance:
        :param address_id:
        :param cart_type: cart, sku
        :param pay_type:
        :param cart_list:
        :param sku_list:
        :param user_note:
        :param ext:
        :param coupon_code:
        :return:
        """

    def confirm_order(self, user_id, clientip, platform, order_id):
        """
        订单确认,收获
        :param user_id:
        :param clientip:
        :param platform:
        :param order_id:
        :return:
        """

    def cancel_order(self, user_id, clientip, platform, order_id, reason):
        """
        取消订单
        :param user_id:
        :param clientip:
        :param platform:
        :param order_id:
        :param reason:
        :return:
        """

    def pay_now(self, user_id, clientip, platform, order_id, type, use_balance, address_id):
        """获取交易流水号"""

    @handler_decorator(perm='', types={'user_id': str}, plain=False, async=False, finished=True)
    def get_order_list(self, user_id):
        """
        获取用户订单列表
        :param user_id:
        :return:
        """
        pass

    @handler_decorator(perm='', types={'orderno': str}, plain=False, async=False, finished=True)
    def get_order(self, orderno):
        """
        获取订单详情
        :param orderno:
        :return:
        """
        pass

    @handler_decorator(perm=0, types={'client_ip': str, 'pay_params': dict}, plain=False, async=False, finished=True)
    def pay(self, client_ip, pay_params):
        """
        订单支付
        :param client_ip:
        :param pay_params:
        :return:
        """
        pay_params.update({'client_ip': client_ip})
        res = self.context_services.pay_sevice.pay(pay_params)
        return res

    @handler_decorator(perm='', types={'orderno': str}, plain=False, async=False, finished=True)
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
