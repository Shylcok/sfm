#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: pay_service.py
@time: 16/10/22 下午1:26
"""

import traceback
from base_service import BaseService

from payment.pay_processor import PayProcessor

class PayService(BaseService):

    def pay(self, pay_params):
        try:
            pay_params = PayProcessor().build_pay_params(pay_params)
            res = PayProcessor().pay(pay_params)
            return res
        except Exception:
            traceback.print_exc()
            return {'code': 110, 'msg': '支付异常,参数错误'}

    def refund(self, refund_params):
        try:
            ch_id = refund_params['ch_id']
            amount = refund_params['amount']
            desc = refund_params['desc']
            res = PayProcessor().refund(ch_id, amount, desc)
            return res
        except Exception:
            traceback.print_exc()
            return {'code': 111, 'msg': '退款异常, 参数错误'}
