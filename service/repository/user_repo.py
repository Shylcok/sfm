#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: user_repo.py
@time: 16/10/13 下午1:48
"""
from service.repository.base_repo import BaseRepo
import logging
import time

class UserRepo(BaseRepo):
    TABLE_NAME = 'sfm_user'

    def __init__(self):
        logging.info('init UserRepo')

    def select_by_user_id(self, user_id):
        sql = """
            select * from {} where id=%s
        """.format(self.TABLE_NAME)

        return self.db.get(sql, user_id)

    def select_by_mobile(self, mobile):
        sql = """
            select * from {} where mobile=%s
        """.format(self.TABLE_NAME)
        return self.db.get(sql, mobile)

    def select_by_user_name(self, user_name):
        sql = """
            select * from {} where user_name=%s
        """.format(self.TABLE_NAME)
        return self.db.get(sql, user_name)

    def select_by_mobile_pwd_md5(self, mobile, pwd_md5):
        sql = """
            select * from {} WHERE mobile=%s and pwd_md5=%s
        """.format(self.TABLE_NAME)
        return self.db.get(sql, mobile, pwd_md5)

    def select_by_user_name_pwd_md5(self, user_name, pwd_md5):
        sql = """
            select * from {} WHERE user_name=%s and pwd_md5=%s
        """.format(self.TABLE_NAME)
        return self.db.get(sql, user_name, pwd_md5)


    def select_by_user_id_pwd_md5(self, user_id, old_pwd_md5):
        sql = """
            select * from {} WHERE id=%s and pwd_md5=%s
        """.format(self.TABLE_NAME)
        return self.db.get(sql, user_id, old_pwd_md5)

    def insert(self, mobile, pwd_md5):
        sql = """
          insert into {} (mobile, user_name, pwd_md5, register_dt) values (%s, %s, %s, %s)
        """.format(self.TABLE_NAME)
        return self.db.execute_lastrowid(sql, mobile, mobile, pwd_md5, time.time())

    def update_pwd(self, user_id, new_pwd_md5):
        sql = """
            update {} set pwd_md5=%s WHERE id=%s
        """.format(self.TABLE_NAME)
        return self.db.execute_rowcount(sql, new_pwd_md5, user_id)

    def update_user_name(self, user_id, new_user_name):
        sql = """
            update {} set user_name=%s WHERE id=%s
        """.format(self.TABLE_NAME)
        return self.db.execute_rowcount(sql, new_user_name, user_id)
