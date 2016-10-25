#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: repos.py
@time: 16/10/13 下午2:23
"""

from user_repo import UserRepo
from conn import sms_redis


class Repos(object):
    _user_repo = UserRepo()
    _sms_redis = sms_redis

    @property
    def user_repo(self):
        return self._user_repo

    @property
    def sms_redis(self):
        return self._sms_redis
