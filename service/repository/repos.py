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
from address_repo import AddressRepo
from cart_repo import CartRepo
from external_repo import ExternalRepo
from conn import sms_redis



class Repos(object):
    _user_repo = UserRepo()
    _address_repo = AddressRepo()
    _cart_repo = CartRepo()
    _external_repo = ExternalRepo()

    _sms_redis = sms_redis

    @property
    def user_repo(self):
        return self._user_repo

    @property
    def sms_redis(self):
        return self._sms_redis

    @property
    def address_repo(self):
        return self._address_repo

    @property
    def cart_repo(self):
        return self._cart_repo

    @property
    def expernal_repo(self):
        return self._external_repo
