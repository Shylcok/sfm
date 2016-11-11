#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: settings_dev.py
@time: 16/10/12 下午2:15
"""

CONFIG = {
    'DEBUG': False,
    'HTTP': {
        'HOST': '0.0.0.0',
        'PORT': 8089,
    },

    'DATABASE': {
        'HOST': '139.224.44.238',  # '127.0.0.1'
        'PORT': 3307,
        # 'USER': 'root',
        # 'PASSWD': '123456',
        # 'NAME': 'sfm',
        'USER': 'root',
        'PASSWD': 'qwrYlksfnDqrfsa*3weaew',
        'NAME': 'sfm',
    },
    'SMS_REDIS': {  # 短信验证码
        'HOST': '139.224.44.238', #'127.0.0.1',
        'PORT': 6380,
        'DB': 4
    },
    'CELERY_REDIS': {  # 订单定时任务消息
        'HOST': '139.224.44.238',
        'PORT': 6380,
        'DB': 5
    },
    'MONGODB': {
        'HOST': '139.224.44.238',
        'PORT': 27018
    },
    'LOG_PATH': './sfm-8089.log',
    'pay': {
        'app_id': 'app_9CO8q1TGCK00P44G',
        'api_key': 'sk_live_L0CqXLf1SyfL0GO4a9zv1yHS',
    },
    'token_secret_key': 'qksytijhjhhdhha%&*&O&&(*',
    'AESKEY': 'ovgNwKHpqmdOTYgI',
    'sku_url': 'http://139.224.44.238:8890/productApi.apiProduct/detail?skuid=',
}
