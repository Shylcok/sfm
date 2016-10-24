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


class BaseService(object):

    """
    只会执行一次
    """
    context_repos = Repos()
