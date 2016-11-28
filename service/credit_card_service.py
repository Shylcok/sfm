#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: credit_card_service.py
@time: 16/11/14 下午7:35
"""

from base_service import BaseService
from constant import *
import logging
from tornado.gen import coroutine, Return


class CreditCardService(BaseService):
    def __init__(self, services):
        super(CreditCardService, self).__init__(services)

    def create_credit_card(self, user_id):
        card_id = GENERATOR_CREDIT_CARD_ID(user_id)
        logging.info('生成信用卡, 卡号:%s' % card_id)
        res = self.context_repos.credit_card_repo.insert(user_id, card_id, CREDIT_CARD_AMOUNT)
        return res

    @coroutine
    def detail(self, user_id, type, page, count):
        credit_card = self.context_repos.credit_card_repo.select(user_id)
        if credit_card is None:
            self.services.credit_card_service.create_credit_card(user_id)
        credit_card = self.context_repos.credit_card_repo.select(user_id)
        credit_card_id = credit_card['card_id']
        if type == "all":
            orders, total = yield self.context_repos.order_repo.select_by_credit_card_id_all(credit_card_id, page, count)
        elif type == "need_pay":
            orders, total = yield self.context_repos.order_repo.select_by_credit_card_id_need_pay(credit_card_id, page, count)
        elif type == "over_time":
            orders, total = yield self.context_repos.order_repo.select_by_credit_card_id_over_time(credit_card_id, page,
                                                                                                  count)
        elif type == "has_pay":
            orders, total = yield self.context_repos.order_repo.select_by_credit_card_id_has_pay(credit_card_id, page,
                                                                                                  count)

        for order in orders:
            order_id = order['order_id']
            skus = yield self.context_repos.sku_order_repo.select_by_order_id(order_id)
            order['skus'] = skus
            order['refund_time'] = int(order['ctime']) + int(CONST_CARD_BORROW_DURATION)

        credit_card.update({'orders': orders})
        res = {'credit_card': credit_card, 'pagination': self.pagination(total, page, count)}
        raise Return(res)

    @coroutine
    def update_related_credit_card_for_borrow(self, order_id):
        order_info = yield self.context_repos.order_repo.select_by_order_id(order_id)
        card_id = order_info['credit_card_id']
        cost_amount = order_info['credit_amount']
        res = self.context_repos.credit_card_repo.update(cost_amount, card_id)
        """借款信息送入消息队列"""
        self.services.order_overtime_task_service.card_borrow_celery(order_id, card_id)
        raise Return(res)

    @coroutine
    def update_related_credit_card_for_pay(self, order_id):
        order_info = yield self.context_repos.order_repo.select_by_order_id(order_id)
        card_id = order_info['credit_card_id']
        cost_amount = order_info['credit_amount']
        refund = -cost_amount
        res = self.context_repos.credit_card_repo.update(refund, card_id)
        """借款信息从消息队列销毁"""
        self.services.order_overtime_task_service.card_pay_celery(order_id, card_id)
        raise Return(res)

    """--------------后台------------------"""

    @coroutine
    def get_credit_cards(self, u_name, u_mobile, channel, update_time_st, update_time_dt, page,
                         count):
        user_cards, total = yield self.context_repos.credit_card_repo.select_user_card(u_name, u_mobile, channel, update_time_st, update_time_dt, page, count)
        res = {'credit_cards': user_cards, 'pagination': self.pagination(total, page, count)}
        raise Return(res)

    @coroutine
    def set_card_amount(self, card_id, inc_amount):
        res = yield self.context_repos.credit_card_repo.set_card_amount(card_id, inc_amount)
        raise Return(res)

    @coroutine
    def get_card_detail(self, card_id, page, count):
        card_info = yield self.context_repos.credit_card_repo.select_by_card_id(card_id)
        user_id = card_info['user_id']
        user_info = self.context_repos.user_repo.select_by_user_id(user_id)
        card_order_infos, total = yield self.context_repos.order_repo.select_by_credit_card_id_all(card_id, page, count)
        card_log_infos = self.context_repos.operate_log_repo.select_by_target_id(card_id)
        res = {
            'user_info': user_info,
            'card_info': card_info,
            'card_order_infos': card_order_infos,
            'card_order_pagination': self.pagination(total, page, count),
            'card_log_infos': card_log_infos
        }
        raise Return(res)


