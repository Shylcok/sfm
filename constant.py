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

"""这里注意,一般mysql中的期限要小于消息队列中的期限, 避免支付过程中,解库存了"""
CONST_ORDER_OVER_DURATION = 5 * 60  # 订单过期时间:30分钟, mysql
CONST_ORDER_OVER_DURATION_CELERY = 60 * 6  # 60 * 30 # 订单过期时间 30 分钟, 任务队列30分钟后执行
CONST_ORDER_OVER_DURATION_CELERY_RETRY = 3  # 3s后继续尝试
CONST_ORDER_SHIP_AMOUNT = 0  # 1000  # 默认邮费 10 元

"""催款消息队列"""
CONST_CARD_BORROW_DURATION_CELERY = 60 * 1  # 60 * 60 * 24 * 60 # 60天后进行一次催款


# 订单号
def GENERATOR_ORDER_ID(user_id):
    return str(int(time.time())) + user_id


# 首付卡ID
def GENERATOR_CREDIT_CARD_ID(user_id):
    ID = '216' + str(int(time.time())) + str(user_id)
    return ID[0: 15]

CREDIT_CARD_AMOUNT = 66600  # 666 元
CREDIT_CARD_DELAY = 60 * 60 * 24 * 60  # 60天

TARGET_TYPE_PAY = 'pay'
TARGET_TYPE_CARD = 'card'
