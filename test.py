#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: test.py
@time: 16/11/24 下午2:07
"""

import tornado
from tornado.ioloop import IOLoop
import contextlib
from tornado.gen import coroutine
from tornado import httpclient
from tornado.gen import Return

@coroutine
def descrease_stock():
    print "====>desc"
    response = yield httpclient.AsyncHTTPClient().fetch('http://www.baidu.com')
    print "<====desc"
    raise Return(True)
    # raise RuntimeError('shibai')


@coroutine
def increase_stock():
    print "====>increase"
    response = yield httpclient.AsyncHTTPClient().fetch('http://www.baidu.com')
    print "<====increase"


class CommitOrderError(Exception):
    def __init__(self, value):
        self.value = value


@contextlib.contextmanager
def make_content():
    res = IOLoop.current().run_sync(lambda: descrease_stock())
    print res
    try:
        yield {}
    except CommitOrderError, err:
        IOLoop.current().run_sync(lambda: increase_stock())

try:
    with make_content() as value:
        print "=======ok"
        raise CommitOrderError('。。。失败')

except RuntimeError, err:
    print err.message

