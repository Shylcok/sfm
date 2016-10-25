#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: services.py
@time: 16/10/13 下午2:28
"""

from user_service import UserService
from cart_service import CartService
from order_service import OrderService
from pay_service import PayService
from webhooks_service import WebhooksService

class Services(object):
    _user_service = UserService()
    _cart_service = CartService()
    _order_service = OrderService()
    _pay_service = PayService()
    _webhooks_service = WebhooksService()

    @property
    def user_service(self):
        return self._user_service

    @property
    def cart_service(self):
        return self._cart_service

    @property
    def order_service(self):
        return self._order_service

    @property
    def pay_sevice(self):
        return self._pay_service

    @property
    def webhooks_service(self):
        return self._webhooks_service