#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: pay_processor.py
@time: 16/10/22 上午11:44
"""
import pingpp
from settings import *
import logging

import base64
import os
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
import time


class PayProcessor(object):
    def __init__(self):
        pingpp.api_key = 'sk_live_L0CqXLf1SyfL0GO4a9zv1yHS'
        pingpp.private_key_path = os.path.dirname(__file__) + 'your_rsa_private_key.pem'

    @staticmethod
    def pay(params):
        logging.info('支付参数: ' + str(params))
        response_charge = pingpp.Charge.create(api_key=pingpp.api_key, **params)
        """
        Ping++ 收到支付请求后返回给你的服务器一个 Charge 对象，我们称这个 Charge 对象为支付凭据;
        你的服务器需要按照 JSON 字符串格式将支付凭据返回给你的客户端，Ping++ SDK 对此做了相应的处理，
        你只需要将获得的支付凭据直接传给客户端。客户端接收后使用该支付凭据用于调起支付控件，而支付凭据的传送方式需要你自行实现。
        """
        logging.info('Ping++支付凭据: ' + str(response_charge))
        return response_charge

    @staticmethod
    def refund(ch_id, amount, refund_desc):
        logging.info('退款参数: 已付款的chargeid %s, 金额 %s, 描述 %s ' % (ch_id, amount, refund_desc))
        ch = pingpp.Charge.retrieve("ch_id")  # ch_id 是已付款的订单号
        res = ch.refunds.create(description=refund_desc, amount=amount)
        logging.info(res)
        return res

    @staticmethod
    def decode_base64(data):
        remainder = len(data) % 4
        if remainder:
            data += '=' * (4 - remainder)
        return base64.decodestring(data.encode('utf-8'))

    @staticmethod
    def verify(data, sig):
        signs = PayProcessor().decode_base64(sig)
        data = data.decode('utf-8') if hasattr(data, "decode") else data
        pubkeystr = open(os.path.join(os.path.dirname(__file__),
                         'your_rsa_public_key.pem')).read()
        pubkey = RSA.importKey(pubkeystr)
        digest = SHA256.new(data.encode('utf-8'))
        pkcs = PKCS1_v1_5.new(pubkey)
        return pkcs.verify(digest, signs)







