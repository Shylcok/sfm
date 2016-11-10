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
        self.channel_ids = {
            'alipay_pc_direct': 1, # 支付宝
            'wx_pub_qr': 0, # 额度卡
            'upacp': 50,
        }

    def verify(self, data, sig):
        return PayProcessor().verify(data, sig)

    def pingpp(self, request_body):
        event = request_body
        event_type = event['type']
        logging.info('收到webhook:%s' % str(event))
        if event_type == 'charge.succeeded':
            """处理支付成功的逻辑"""

            order_data = event['data']['object']

            order_id = order_data['order_no']
            amount = order_data['amount']
            water_id = order_data['transaction_no']
            channel_id = self.channel_ids[order_data['channel']]
            channel_water_id = order_data['id']
            time = order_data['time_paid']
            event['_id'] = event['id']
            self.context_repos.pay_mongodb.insert(event)
            self.context_repos.pay_repo.insert(water_id, channel_id, channel_water_id, amount, order_id, time)
            self.context_repos.order_repo.update_state_1(order_id)
            logging.info('支付webhook处理成功')
            return {'code': 0, 'msg': '付款成功'}
        elif type == 'refund.succeeded':
            # TODO: 处理退款成功的逻辑
            return {'code': 0, 'msg': '退款成功'}
        else:
            logging.info('webhooks错误: %s' % str(event))

        return {'status_code': 500, 'code': -1, 'msg': '处理失败'}


