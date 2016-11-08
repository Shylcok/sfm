#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: base_service.py
@time: 16/10/12 下午2:07
"""

from repository import *
from concurrent.futures import ThreadPoolExecutor


class BaseService(object):

    """
    只会执行一次
    """
    executor = ThreadPoolExecutor(50)
    context_repos = Repos()

    def __init__(self, services):
        self.services = services

