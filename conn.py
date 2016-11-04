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


# 验证码 redis 缓存
SMS_REDIS_CONFIG = CONFIG['SMS_REDIS']
# sms_redis = redis.Redis(host=SMS_REDIS_CONFIG['HOST'], port=SMS_REDIS_CONFIG['PORT'], db=SMS_REDIS_CONFIG['DB'])
sms_redis_pool = redis.ConnectionPool(host=SMS_REDIS_CONFIG['HOST'], port=SMS_REDIS_CONFIG['PORT'],
                                      db=SMS_REDIS_CONFIG['DB'])
sms_redis = redis.Redis(connection_pool=sms_redis_pool)  # 直接建立一个连接池，然后作为参数Redis，这样就可以实现多个Redis实例共享一个连接池

# 订单定时任务 redis 缓存
CELERY_REDIS_CONFIG = CONFIG['CELERY_REDIS']
celery_redis_pool = redis.ConnectionPool(host=CELERY_REDIS_CONFIG['HOST'], port=CELERY_REDIS_CONFIG['PORT'],
                                         db=CELERY_REDIS_CONFIG['DB'])
celery_redis = redis.Redis(connection_pool=celery_redis_pool)  # 直接建立一个连接池，然后作为参数Redis，这样就可以实现多个Redis实例共享一个连接池
