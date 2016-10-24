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
from settings import CONFIG

DATABASE = CONFIG['DATABASE']

db = torndb.Connection('%s:%s' % (DATABASE['HOST'], DATABASE['PORT']),
                       DATABASE['NAME'], user=DATABASE['USER'],
                       password=DATABASE['PASSWD'], max_idle_time=100,
                       charset='utf8mb4', time_zone="+8:00"
                       )