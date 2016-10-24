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



class PayProcessor(object):
    def __init__(self):
        pingpp.api_key = 'sk_live_L0CqXLf1SyfL0GO4a9zv1yHS'
        pingpp.private_key_path = os.path.dirname(__file__) + 'your_rsa_private_key.pem'

    @staticmethod
    def build_pay_params(pay_params):
        pay_info = {}
        pay_info['order_no'] = pay_params['orderno']   # 11 位 商户订单号，适配每个渠道对此参数的要求，必须在商户系统内唯,alipay : 1-64 位，  wx : 2-32 位
        pay_info['app'] = dict(id=CONFIG['pay']['app_id'])  # 支付使用的  app 对象的  id
        pay_info['channel'] = pay_params['channel']  # alipay_pc_direct	支付宝 PC 网页支付;wx_pub_qr 微信公众号扫码支付
        pay_info['amount'] = pay_params['amount']  # 订单总金额（必须大于0
        pay_info['currency'] = 'cny'  # 三位 ISO 货币代码，目前仅支持人民币  cny 。
        pay_info['client_ip'] = pay_params['client_ip']
        pay_info['subject'] = pay_params['subject']  # 商品的标题，该参数最长为 32 个 Unicode 字符
        pay_info['body'] = pay_params['body']  # 商品的描述信息，该参数最长为 128 个 Unicode 字符
        if pay_params['channel'] == 'alipay_pc_direct':
            pay_info['extra'] = dict(
                success_url=pay_params['success_url']  # 支付成功的回调地址。到达付款成功页面
            )
        elif pay_params['channel'] == 'wx_pub_qr':
            pay_info['extra'] = dict(
                product_id=pay_params['product_id']
            )
        return pay_info

    @staticmethod
    def pay(params):
        logging.info('支付参数: ' + str(params))
        response_charge = pingpp.Charge.create(api_key=pingpp.api_key, **params)
        logging.info('支付返回: ' + str(response_charge))
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







