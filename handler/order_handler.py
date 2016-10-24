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

    """-------------前端用户接口----------------"""


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


    @handler_decorator(perm='', types={'client_ip': str, 'pay_params': dict}, plain=False, async=False, finished=True)
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
