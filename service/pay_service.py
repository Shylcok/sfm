#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: pay_service.py
@time: 16/10/22 下午1:26
"""

import traceback
from base_service import BaseService

from payment.pay_processor import PayProcessor
from settings import CONFIG
from tornado.gen import coroutine
from tornado.gen import Return
import random

class PayService(BaseService):
    def __init__(self, services):
        super(PayService, self).__init__(services)

    @coroutine
    def pay(self, client_ip, user_id, pay_params):
        order_id = pay_params['order_id']
        channel = pay_params['channel']
        success_url = pay_params['success_url']
        order_info = yield self.context_repos.order_repo.select_by_order_id_user_id(order_id, user_id)
        orders_info = yield self.context_repos.sku_order_repo.select_by_order_id(order_id)

        pay_info = {}
        pay_info['order_no'] = order_id  # 11 位 商户订单号，适配每个渠道对此参数的要求，必须在商户系统内唯,alipay : 1-64 位，  wx : 2-32 位
        pay_info['app'] = dict(id=CONFIG['pay']['app_id'])  # 支付使用的  app 对象的  id
        pay_info['channel'] = channel  # alipay_pc_direct	支付宝 PC 网页支付;wx_pub_qr 微信公众号扫码支付
        pay_info['amount'] = order_info['pay_amount']  # 订单总金额（必须大于0
        pay_info['currency'] = 'cny'  # 三位 ISO 货币代码，目前仅支持人民币  cny 。
        pay_info['client_ip'] = client_ip
        pay_info['subject'] = "商品"  # 商品的标题，该参数最长为 32 个 Unicode 字符
        pay_info['body'] = orders_info[0]['sku_name']  # 商品的描述信息，该参数最长为 128 个 Unicode 字符
        pay_info['time_expire'] = order_info['overtime']  # 订单失效时间
        pay_info['metadata'] = {}
        pay_info['metadata']['type'] = 'order_pay'

        if pay_params['channel'] == 'alipay_pc_direct':
            pay_info['extra'] = dict(
                success_url=success_url  # 支付成功的回调地址。到达付款成功页面
            )
        elif pay_params['channel'] == 'wx_pub_qr':
            pay_info['extra'] = dict(
                product_id=orders_info[0]['sku_id']
            )
        res = PayProcessor().pay(pay_info)
        raise Return(res)

    @coroutine
    def pay_credit_card(self, client_ip, user_id, pay_params):
        order_id = pay_params['order_id']
        channel = pay_params['channel']
        success_url = pay_params['success_url']
        order_info = self.context_repos.order_repo.select_by_order_id(order_id)
        if order_info['state'] == 1 and order_info['credit_card_state'] == 0:
            credit_amount = -order_info['credit_amount']
        else:
            raise Return({'code': 310, 'msg': '订单状态不正确, 不能进行还卡'})

        pay_info = {}
        pay_info['order_no'] = order_id + order_info['credit_card_id'][-5:-1]  # 11 位 商户订单号，适配每个渠道对此参数的要求，必须在商户系统内唯,alipay : 1-64 位，  wx : 2-32 位
        pay_info['app'] = dict(id=CONFIG['pay']['app_id'])  # 支付使用的  app 对象的  id
        pay_info['channel'] = channel  # alipay_pc_direct	支付宝 PC 网页支付;wx_pub_qr 微信公众号扫码支付
        pay_info['amount'] = credit_amount  # 还款总金额（必须大于0
        pay_info['currency'] = 'cny'  # 三位 ISO 货币代码，目前仅支持人民币  cny 。
        pay_info['client_ip'] = client_ip
        pay_info['subject'] = "额度卡还款"  # 商品的标题，该参数最长为 32 个 Unicode 字符
        pay_info['body'] = '额度卡号:%s' % order_info['credit_card_id']  # 商品的描述信息，该参数最长为 128 个 Unicode 字符
        # pay_info['time_expire'] = 0  # 订单失效时间 #  mall 每次支付重启一个新订单, 我们也应该这样,不过时间应该按照商品如订单表时间算过期
        pay_info['metadata'] = {}
        pay_info['metadata']['type'] = 'card_pay'
        pay_info['metadata']['credit_card_id'] = order_info['credit_card_id']
        if pay_params['channel'] == 'alipay_pc_direct':
            pay_info['extra'] = dict(
                success_url=success_url  # 支付成功的回调地址。到达付款成功页面
            )
        elif pay_params['channel'] == 'wx_pub_qr':
            pay_info['extra'] = dict(
                product_id=pay_params['product_id']
            )
        res = PayProcessor().pay(pay_info)
        raise Return(res)

    def refund(self, refund_params):
        try:
            ch_id = refund_params['ch_id']
            amount = refund_params['amount']
            desc = refund_params['desc']
            res = PayProcessor().refund(ch_id, amount, desc)
            return res
        except Exception:
            traceback.print_exc()
            return {'code': 111, 'msg': '退款异常, 参数错误'}
