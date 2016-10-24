#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: order_service.py
@time: 16/10/14 下午8:03
"""

from base_service import BaseService

class OrderService(BaseService):

    def get_user(self, user_id):
        res = self.context_repos.user_repo.select_by_user_id(user_id)
        return res