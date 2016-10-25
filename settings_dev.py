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
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'root',
        'PASSWD': '123456',
        'NAME': 'sfm',
    },
    'SMS_REDIS': {  # 短信验证码
        'HOST': '127.0.0.1',
        'PORT': 6379,
        'DB': 4
    },

    'LOG_PATH': './sfm-8089.log',
    'pay': {
        'app_id': 'app_9CO8q1TGCK00P44G',
        'api_key': 'sk_live_L0CqXLf1SyfL0GO4a9zv1yHS',
    },

    'token_secret_key': 'qksytijhjhhdhha%&*&O&&(*',
    'AESKEY': 'ovgNwKHpqmdOTYgI',

}
