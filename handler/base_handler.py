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
    """ 属于类成员变量, 进程中只会存在一个,注意线程安全,
     1.python 虽然有GIL,但是这个只是针对一条字节码作为原子操作来说的,
     2.执行语句本身可能存在先后顺序,导致线程不安全,
     3.一般情况下list dict 存储等是线程安全的,
     4.redis连接实例是线程安全的,可以直接将redis连接实例设置为一个全局变量,直接使用,
     5.MySQLdb线程安全, 线程友好，线程间不会相互阻塞, torndb也是基于MySQLdb,
     6.celery The application is thread-safe so that multiple Celery applications with different configurations, components and tasks can co-exist in the same process space."""
    context_services = Services()

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)