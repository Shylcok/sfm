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


class BaseRepo(object):

    executor = ThreadPoolExecutor(50)

    """属性装饰器,保证只读"""
    @property
    def db(self):
        return DB
