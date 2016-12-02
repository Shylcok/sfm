#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: order_overtime_task_service.py
@time: 16/11/3 下午11:57
"""
import sys

sys.path.append(sys.path[0] + '/../')

from base_service import BaseService
from constant import *
from celery import Celery
import logging
from tornado.gen import coroutine
import sms

celery = Celery('tasks', broker='redis://127.0.0.1:6379/0')


class OrderOvertimeTaskService(BaseService):
    def __init__(self, services):
        super(OrderOvertimeTaskService, self).__init__(services)

    @coroutine
    def process_over_time(self, order_id):
        # 开始支付, check state=0 and set state=99 订单进入支付状态
        # 支付成功, check state=1.5 and set state=1 订单进入成功支付状态
        # 支付异常, check state=1.5 and set state=0 订单进入未支付状态
        # 暂时不需要了,因为设置了支付时间短于过期时间

        # check state=0 and set state=5 订单过期,
        res = yield self.context_repos.order_repo.update_state_5(order_id)
        logging.info('订单过期, order_id=%s, exe_row_count=%s' % (order_id, res))
        # 解订单库存
        yield self.services.order_service.increase_stocks(order_id)

    def commit_order_celery(self, order_id):
        """
        下单时, 订单进入队列
        :param order_id:
        :return:
        """
        push_task_id = celery.send_task('tasks.exec_task_order_overtime'
                                        , [order_id]
                                        , countdown=CONST_ORDER_OVER_DURATION_CELERY)  # 推送消息
        self.context_repos.celery_redis.set(order_id, push_task_id, CONST_ORDER_OVER_DURATION_CELERY)
        logging.info('开始一个新的订单任务, order_id=%s, push_task_id=%s' % (order_id, push_task_id))

    def after_pay_celery(self, order_id):
        """
        支付后, 去除消息队列中的订单
        :param order_id:
        :return:
        """
        push_task_id = self.context_repos.celery_redis.get(order_id)
        celery.control.revoke(push_task_id, terminate=True)
        self.context_repos.celery_redis.delete(order_id)
        logging.info('支付完后取消订单, 任务队列和redis中task 清除, order_id=%s, push_task_id=%s' % (order_id, push_task_id))

    @coroutine
    def process_remind_card_notify(self, order_id):
        order_info = yield self.context_repos.order_repo.select_by_order_id(order_id)
        card_amount = order_info['credit_amount']
        order_id = order_info['order_id']
        mobile = self.context_repos.user_repo.select_by_user_id(order_info['user_id'])
        msg = '你有一条还款已达到60天, 订单号:%s, 还款金额:%s' % (order_id, -card_amount)
        success = sms.send_sms(msg, mobile)
        if success:
            logging.info('发送催款短信, order_id=%s, msg=%s, mobile=%s' % (order_id, msg, mobile))
        else:
            logging.error('发送催款短信失败, order_id=%s, msg=%s, mobile=%s' % (order_id, msg, mobile))

    def card_borrow_celery(self, order_id, card_id):
        """
        首付卡借款后, 进入队列
        :param card_id:
        :param order_id:
        :return:
        """
        push_task_id = celery.send_task('tasks.exec_task_card_borrow'
                                        , [order_id]
                                        , countdown=CONST_CARD_BORROW_DURATION_CELERY)  # 推送消息
        order_card_id = order_id + card_id
        self.context_repos.celery_redis.set(order_card_id, push_task_id, CONST_CARD_BORROW_DURATION_CELERY)
        logging.info('开始一个新的催款任务, order_id=%s, card_id=%s, push_task_id=%s, redis_order_card_id=%s' % (
        order_id, card_id, push_task_id, order_card_id))

    def card_pay_celery(self, order_id, card_id):
        """
        首付卡还款后, 去除消息队列
        :param card_id:
        :param order_id:
        :return:
        """
        order_card_id = order_id + card_id
        push_task_id = self.context_repos.celery_redis.get(order_card_id)
        celery.control.revoke(push_task_id, terminate=True)
        self.context_repos.celery_redis.delete(order_card_id)
        logging.info('取消催款, 任务队列和redis中task 清除, order_id=%s, card_id=%s, push_task_id=%s, order_card_id=%s' % (
        order_id, card_id, push_task_id, order_card_id))


if __name__ == "__main__":
    service = OrderOvertimeTaskService(object)
    service.commit_order_celery('1119')
