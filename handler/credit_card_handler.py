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


class CreditCardHandler(BaseHandler):

    @gen.coroutine
    @handler_decorator(perm=1, types={'user_id': str}, plain=False, async=True, finished=True)
    def detail(self, user_id):
        """
        获取额度卡信息
        :param user_id:
        :return:
        """
        res = yield self.context_services.credit_card_service.detail(user_id)
        raise gen.Return(res)