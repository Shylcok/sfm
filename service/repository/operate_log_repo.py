#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: operate_log_repo.py
@time: 16/11/28 上午11:12
"""


from service.repository.base_repo import BaseRepo
from constant import *
import logging


class OperateLogRepo(BaseRepo):
    TABLE_NAME = 'sfm_operate_log'

    def __init__(self, *args):
        logging.info('init operator repo')
        super(OperateLogRepo, self).__init__(args)

    def insert(self, user_id, target_id, target_type, log):
        sql = """
            insert into {} set user_id=%s, target_id=%s, target_type=%s, log=%s, time=%s
        """.format(self.TABLE_NAME)
        res = self.db.insert(sql, user_id, target_id, target_type, log, time.time())
        return res

    def select_by_target_id(self, target_id):
        sql = """
            select * from {} where target_id=%s
        """.format(self.TABLE_NAME)
        res = self.db.query(sql, target_id)
        return res

