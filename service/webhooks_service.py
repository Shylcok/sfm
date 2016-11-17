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
from tornado.gen import Return, coroutine

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

    @coroutine
    def pingpp(self, request_body):
        event = request_body
        event_type = event['type']
        logging.info('收到webhook:%s' % str(event))
        if event_type == 'charge.succeeded':
            """处理支付成功的逻辑"""
            order_data = event['data']['object']
            pay_type = order_data['metadata']['type']

            if pay_type == "order_pay":
                """处理下单支付"""
                order_id = order_data['order_no']
                amount = order_data['amount']
                water_id = order_data['transaction_no']
                channel_id = self.channel_ids[order_data['channel']]
                channel_water_id = order_data['id']
                time = order_data['time_paid']
                event['_id'] = event['id']
                """支付信息保存"""
                has_mongodb_pay = self.context_repos.pay_mongodb.find({'_id': event['id']})
                # TODO: 控制并发引起多次调用webhook,没有加锁
                if has_mongodb_pay is not None:
                    raise Return({'code': 0, 'msg': '消息已经接过过'})
                self.context_repos.pay_mongodb.insert(event)
                self.context_repos.pay_repo.insert(water_id, channel_id, channel_water_id, amount, order_id, time)
                logging.info('webhook====> 支付信息保存, water_id= %s' % water_id)
                """订单状态更新;这里有问题, 更新订单状态 完成支付的时候,订单状态应该在支付中, 防止订单在支付的时候被解库存; 或者支付时间期限要短于过期时间"""
                self.context_repos.order_repo.update_state_1(order_id)
                logging.info('webhook====> 订单状态更新, order_id= %s' % order_id)

                yield self.services.credit_card_service.update_related_credit_card(order_id)
                logging.info('webhook====> 首付卡remain_amount更新, 并将催款信息送入消息队列')

                """订单过期消息删除"""
                self.services.order_overtime_task_service.after_pay_celery(order_id)
                logging.info('webhook====> 过期消息队列删除, order_id= %s' % order_id)

                logging.info('webhook=============> 支付回调处理成功')
                raise Return({'code': 0, 'msg': '付款成功'})
            elif pay_type == "card_pay":
                """处理还款支付逻辑"""
                pass

        elif type == 'refund.succeeded':
            # TODO: 处理退款成功的逻辑
            raise Return({'code': 0, 'msg': '退款成功'})
        else:
            logging.info('webhooks错误: %s' % str(event))

        raise Return({'status_code': 500, 'code': -1, 'msg': '处理失败'})


