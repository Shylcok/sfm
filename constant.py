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

CONST_ORDER_OVER_DURATION = 30 * 60  # 订单过期时间:30分钟, mysql
CONST_ORDER_OVER_DURATION_CELERY = 6 * 1  # 订单过期时间 30 分钟, 任务队列30分钟后执行
CONST_ORDER_OVER_DURATION_CELERY_RETRY = 3 # 3s后继续尝试
CONST_ORDER_SHIP_AMOUNT = 1000  # 默认邮费 10 元


# 订单号
def GENERATOR_ORDER_ID(user_id):
    return str(int(time.time())) + user_id
