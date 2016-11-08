#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: external_repo.py
@time: 16/11/1 下午10:52
"""

import tornado
from settings import CONFIG
import json
from tornado.gen import coroutine
from tornado import gen
import traceback
import logging

class ExternalRepo(object):

    @coroutine
    def get_sku_info(self, sku_id):
        client = tornado.httpclient.AsyncHTTPClient()
        request = tornado.httpclient.HTTPRequest(
            url=CONFIG['sku_url'] + sku_id,
            method="GET",
        )
        response = yield tornado.gen.Task(client.fetch, request)
        body_dic = json.loads(response.body)
        if body_dic['code'] == 0:
            raise gen.Return(body_dic['data'])
        else:
            raise gen.Return(False)

    @coroutine
    def decrease_stock(self, sku_id, sku_count):
        """
        锁库存
        :param sku_id:
        :param sku_count:
        :return:
        """
        logging.info('===> decrease_stock sku_id=%s, sku_count=%s' % (sku_id, sku_count))
        raise gen.Return(True)

    @coroutine
    def increase_stock(self, sku_id, sku_count):
        """
        解库存
        :param sku_id:
        :param sku_count:
        :return:
        """
        logging.info('===> increase_stock sku_id=%s, sku_count=%s' % (sku_id, sku_count))
        raise gen.Return(True)
