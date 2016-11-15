#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: base_repo.py
@time: 16/10/12 下午2:11
"""

from conn import db as DB
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
import torndb


class Transaction(object):

    def __enter__(self):
        DB._ensure_connected()
        DB._db.autocommit(False)

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            # OperationalError时数据库连接已关闭
            if exc_type is not torndb.OperationalError:
                DB._db.rollback()
            else:
                raise
        else:
            DB._db.commit()
        DB._db.autocommit(True)

    def __call__(self, func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapped


def transaction(func=None):
    if func:
        return Transaction()(func)
    else:
        return Transaction()


class BaseRepo(object):

    executor = ThreadPoolExecutor(50)

    """属性装饰器,保证只读"""
    @property
    def db(self):
        DB.reconnect()
        return DB