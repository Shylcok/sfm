#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: webhooks_handler.py
@time: 16/10/22 下午3:41
"""

from base_handler import *
import base64
import json


class WebhookHandler(BaseHandler):
    """
    订单处理
    """

    @handler_decorator(perm='', types={},
                       plain=False, async=False, finished=True)
    def pingpp(self):
        data = json.loads(self.request.body)
        sig = self.request.headers.get('x-pingplusplus-signature')
        res = self.context_services.webhooks_service.pingpp(data, sig)
        return res
