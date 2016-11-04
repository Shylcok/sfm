#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: setting_prod.py
@time: 16/10/12 下午2:39
"""


CONFIG = {
    'DEBUG': False,

    'HTTP': {
        'HOST': '0.0.0.0',
        'PORT': 8089,
    },

    'SMS_REDIS': {  # 短信验证码
        'HOST': '127.0.0.1',
        'PORT': 6379,
        'DB': 4
    },
    'CELERY_REDIS': {  # 订单定时任务消息
        'HOST': '127.0.0.1',
        'PORT': 6379,
        'DB': 5
    },
    'DATABASE': {
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'root',
        'PASSWD': 'qwrYlksfnDqrfsa*3weaew',
        'NAME': 'sfm',
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
