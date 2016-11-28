#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: auth_repo.py
@time: 16/11/28 下午4:10
"""


import logging
from base_repo import BaseRepo
from tornado.concurrent import run_on_executor
import time


class AuthRepo(BaseRepo):
    TABLE_NAME = 'sfm_auth'

    def __init__(self, *args):
        logging.info('init AuthRepo')
        super(AuthRepo, self).__init__(*args)

    def select_by_user_id(self, user_id):
        sql = """
            select * from {} where user_id=%s
        """.format(self.TABLE_NAME)
        res = self.db.get(sql, user_id)
        return res

    def insert(self, user_id, real_name, id_code, id_card_up, id_card_down):
        sql = """
            insert into {} values(null, %s, %s, %s, %s, %s, %s, 0, '') on duplicate key update real_name=%s, id_code=%s, id_card_up=%s, id_card_down=%s, time=%s, pass=0
        """.format(self.TABLE_NAME)
        res = self.db.execute_rowcount(sql, user_id, real_name, id_code, id_card_up, id_card_down, time.time()
                                       , real_name, id_code, id_card_up, id_card_down, time.time())
        return res

    def update_by_user_id(self, user_id, is_pass, note):
        sql = """
            update {} set pass=%s, note=%s where user_id=%s
        """.format(self.TABLE_NAME)
        res = self.db.execute_rowcount(sql, is_pass, note, user_id)
        return res


