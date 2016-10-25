#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: conn.py
@time: 16/10/12 下午2:14
"""

import torndb
import redis
from settings import CONFIG

DATABASE = CONFIG['DATABASE']

db = torndb.Connection('%s:%s' % (DATABASE['HOST'], DATABASE['PORT']),
                       DATABASE['NAME'], user=DATABASE['USER'],
                       password=DATABASE['PASSWD'], max_idle_time=100,
                       charset='utf8mb4', time_zone="+8:00"
                       )

SMS_REDIS_CONFIG = CONFIG['SMS_REDIS']
# sms_redis = redis.Redis(host=SMS_REDIS_CONFIG['HOST'], port=SMS_REDIS_CONFIG['PORT'], db=SMS_REDIS_CONFIG['DB'])
redis_pool = redis.ConnectionPool(host=SMS_REDIS_CONFIG['HOST'], port=SMS_REDIS_CONFIG['PORT'],
                                  db=SMS_REDIS_CONFIG['DB'])
sms_redis = redis.Redis(connection_pool=redis_pool)  # 直接建立一个连接池，然后作为参数Redis，这样就可以实现多个Redis实例共享一个连接池
