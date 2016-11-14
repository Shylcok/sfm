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
from constant import GENERATOR_CREDIT_CARD_ID, CREDIT_CARD_AMOUNT
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
    def detail(self, user_id):
        credit_card = self.context_repos.credit_card_repo.select(user_id)
        credit_card_id = credit_card['card_id']
        orders = yield self.context_repos.order_repo.select_by_credit_card_id(credit_card_id)
        credit_card.update({'orders': orders})
        raise Return(credit_card)

    @coroutine
    def update_related_credit_card(self, order_id):
        order_info = yield self.context_repos.order_repo.select_by_order_id(order_id)
        card_id = order_info['credit_card_id']
        cost_amount = order_info['card_amount']
        res = self.context_repos.credit_card_repo.update(cost_amount, card_id)
        raise Return(res)


