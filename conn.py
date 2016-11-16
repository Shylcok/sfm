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
import pymongo
from settings import CONFIG

"""mysql数据库连接"""
DATABASE = CONFIG['DATABASE']
db = torndb.Connection('%s:%s' % (DATABASE['HOST'], DATABASE['PORT']),
                       DATABASE['NAME'], user=DATABASE['USER'],
                       password=DATABASE['PASSWD'], max_idle_time=60,
                       charset='utf8mb4', time_zone="+8:00"
                       )

"""验证码 redis 连接"""
SMS_REDIS_CONFIG = CONFIG['SMS_REDIS']
# sms_redis = redis.Redis(host=SMS_REDIS_CONFIG['HOST'], port=SMS_REDIS_CONFIG['PORT'], db=SMS_REDIS_CONFIG['DB'])
sms_redis_pool = redis.ConnectionPool(host=SMS_REDIS_CONFIG['HOST'], port=SMS_REDIS_CONFIG['PORT'],
                                      db=SMS_REDIS_CONFIG['DB'])
sms_redis = redis.Redis(connection_pool=sms_redis_pool)  # 直接建立一个连接池，然后作为参数Redis，这样就可以实现多个Redis实例共享一个连接池

"""订单定时任务 redis 缓存"""
CELERY_REDIS_CONFIG = CONFIG['CELERY_REDIS']
celery_redis_pool = redis.ConnectionPool(host=CELERY_REDIS_CONFIG['HOST'], port=CELERY_REDIS_CONFIG['PORT'],
                                         db=5)
celery_redis = redis.Redis(connection_pool=celery_redis_pool)  # 直接建立一个连接池，然后作为参数Redis，这样就可以实现多个Redis实例共享一个连接池

"""订单json 详细数据备份 mongodb"""
MONGODB = CONFIG['MONGODB']
mongo_client = pymongo.MongoClient(MONGODB['HOST'], MONGODB['PORT'], connect=False)
mongo_db = mongo_client.sfm

import traceback

if __name__ == "__main__":
    with sms_redis.pipeline() as pipe:
        while 1:
            try:
                #关注一个key
                pipe.watch('stock_count')
                count = int(pipe.get('stock_count'))
                if count > 0:  # 有库存
                    # 事务开始
                    pipe.multi()
                    pipe.set('stock_count', count - 1)
                    # 事务结束
                    pipe.execute()
                    # 把命令推送过去
                break
            except Exception:
                traceback.print_exc()
                continue




