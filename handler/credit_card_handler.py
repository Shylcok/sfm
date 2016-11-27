#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: credit_card_handler.py
@time: 16/11/14 下午7:58
"""

from base_handler import *
from tornado import gen
import time


class CreditCardHandler(BaseHandler):
    @gen.coroutine
    @handler_decorator(perm=1, types={'user_id': str, 'page': int, 'count': int, 'type': str}, plain=False, async=True, finished=True)
    def detail(self, user_id, type, page, count):
        """
        获取额度卡信息
        :param user_id:
        :return:
        """
        res = yield self.context_services.credit_card_service.detail(user_id, type, page, count)
        raise gen.Return(res)

    @gen.coroutine
    @handler_decorator(perm=1, types={'client_ip': str, 'user_id': str, 'pay_params': dict}, plain=False, async=True,
                       finished=True)
    def pay(self, client_ip, user_id, pay_params):
        res = yield self.context_services.pay_sevice.pay_credit_card(client_ip, user_id, pay_params)
        raise gen.Return(res)

    """------------------后台------------------"""

    @gen.coroutine
    @handler_decorator(perm=0, types={'u_name': str, 'u_mobile': str, 'channel': str, 'update_time_st': int,
                                      'update_time_dt': int, 'page': int, 'count': int}, plain=False, async=True,
                       finished=True)
    def get_credit_cards(self, u_name='', u_mobile='', channel='', update_time_st=0, update_time_dt=time.time(), page=1,
                         count=10):
        """
        后台给信用卡数据
        :param u_mobile:
        :param u_name:
        :param channel:
        :param update_time_st:
        :param update_time_dt:
        :param page:
        :param count:
        :return:
        """
        res = yield self.context_services.credit_card_service.get_credit_cards(u_name, u_mobile, channel,
                                                                               update_time_st, update_time_dt, page,
                                                                               count)
        raise gen.Return(res)
