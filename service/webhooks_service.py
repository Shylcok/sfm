#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: webhooks_service.py
@time: 16/10/22 下午3:58
"""


from service.base_service import BaseService
from payment.pay_processor import PayProcessor
import logging

class WebhooksService(BaseService):

    def __init__(self, services):
        super(WebhooksService, self).__init__(services)

    def verify(self, data, sig):
        return PayProcessor().verify(data, sig)

    def pingpp(self, data, sig):
        is_verify = self.verify(data, sig)
        if is_verify:
            if type == 'charge.succeeded':
                # TODO: 处理支付成功的逻辑

                return {'code': 0, 'msg': '付款成功'}
            elif type == 'refund.succeeded':
                # TODO: 处理退款成功的逻辑

                return {'code': 0, 'msg': '退款成功'}
            else:
                logging.info('webhooks错误: %s' % str(data))
        else:
            logging.info('weebhooks验证错误 data:%s, sig: %s' % (str(data), sig))

        return {'status_code': 500, 'code': -1, 'msg': '处理失败'}


