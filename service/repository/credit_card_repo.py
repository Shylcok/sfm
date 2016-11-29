#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: credit_card_repo.py
@time: 16/11/14 下午7:35
"""



from service.repository.base_repo import BaseRepo
import logging
from tornado.concurrent import run_on_executor
import time
from constant import *


class CreditCardRepo(BaseRepo):
    TABLE_NAME = 'sfm_credit_card'

    def __init__(self, *args):
        logging.info('README.md CreditCardRepo')
        super(CreditCardRepo, self).__init__(*args)

    def insert(self, user_id, card_id, amount):
        sql = """
            insert into {} set user_id=%s, card_id=%s, amount=%s, remain_amount=%s
        """.format(self.TABLE_NAME)
        r_count = self.db.execute_rowcount(sql, user_id, card_id, amount, amount)
        self.repos.operate_log_repo.insert(user_id, card_id, OP_LOG.type_card, OP_LOG.get_log_create_card(amount))
        return r_count

    def select(self, user_id):
        sql = """
            select * from {} where user_id=%s
        """.format(self.TABLE_NAME)
        credit_card = self.db.get(sql, user_id)
        return credit_card

    def update(self, cost_amount, card_id):
        sql = """
            update {} set remain_amount=remain_amount+%s where card_id=%s
        """.format(self.TABLE_NAME)
        res = self.db.execute_rowcount(sql, cost_amount, card_id)
        self.repos.operate_log_repo.insert('0', card_id, OP_LOG.type_card, OP_LOG.get_log_update_amount(cost_amount))
        return res

    @run_on_executor
    def select_user_card(self, user_name, mobile, channel, update_time_st, update_time_ed, page, count):
        sql = """
        select user_tb.*, card_tb.* from sfm_user as user_tb
        join sfm_credit_card as card_tb on user_tb.id=card_tb.user_id
        where user_tb.user_name like %s and user_tb.mobile like %s
        and  card_tb.channel like %s and card_tb.update_time<%s and card_tb.update_time>%s
        limit %s,%s
        """
        user_name = '%' + user_name + '%'
        mobile = '%' + mobile + '%'
        channel = '%' + channel + '%'
        res = self.db.query(sql, user_name, mobile, channel, update_time_ed, update_time_st, (page-1)*count, count)
        sql = """
                select 1 from sfm_user as user_tb
                join sfm_credit_card as card_tb on user_tb.id=card_tb.user_id
                where user_tb.user_name like %s and user_tb.mobile like %s
                and  card_tb.channel like %s and card_tb.update_time<%s and card_tb.update_time>%s
                """
        total = self.db.execute_rowcount(sql, user_name, mobile, channel, update_time_ed, update_time_st)
        return res, total

    @run_on_executor
    def set_card_amount(self, card_id, inc_amount):
        sql = """
            update {} set amount=amount+%s, remain_amount=remain_amount+%s, update_time=%s where card_id=%s
        """.format(self.TABLE_NAME)
        res = self.db.execute_rowcount(sql, inc_amount, inc_amount, time.time(), card_id)
        self.repos.operate_log_repo.insert('0', card_id, OP_LOG.type_card, OP_LOG.get_log_set_amount_card(inc_amount))
        return res

    @run_on_executor
    def select_by_card_id(self, card_id):
        sql = """
            select * from {} where card_id=%s
        """.format(self.TABLE_NAME)
        res = self.db.get(sql, card_id)
        return res



