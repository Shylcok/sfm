#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: constant.py
@time: 16/10/25 上午11:47
"""

import time

"""
基本常量
"""
CONST_COOKIE_EXPIRES = 60 * 60 * 12  # 12小时
CONST_COOKIE_USER_TOKEN_NAME = 'sfm_user_token'
CONST_COOKIE_USER_NAME = 'user_name'

CONST_ORDER_OVER_DURATION = 30 * 60  # 30分钟
CONST_ORDER_SHIP_AMOUNT = 1000  # 10 元


# 订单号
def GENERATOR_ORDER_ID(user_id):
    return str(int(time.time())) + user_id
