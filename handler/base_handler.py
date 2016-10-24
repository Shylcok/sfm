#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: core_handler.py
@time: 16/10/13 下午2:05
"""


from core.core_handler import CoreHandler
import logging
from core.handler_decorator import handler_decorator
from service import Services


class BaseHandler(CoreHandler):

    context_services = Services()

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)