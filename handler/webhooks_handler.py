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
    支付回调
    """

    def verify(self):
        data = self.request.body
        sig = self.request.headers.get('x-pingplusplus-signature')
        if sig is None:
            return True
        is_verify = self.context_services.webhooks_service.verify(data, sig)
        if is_verify is False:
            logging.info('weebhooks验证错误 data:%s, sig: %s' % (str(data), sig))
        return is_verify

    @handler_decorator(perm=0, types={},
                       plain=False, async=False, finished=True)
    def pingpp(self):
        """
        支付成功 hook
        :return:
        """
        if self.verify() is False:
            return {'status_code': 500}
        else:
            request_body = json.loads(self.request.body)
            res = self.context_services.webhooks_service.pingpp(request_body)
            return res

