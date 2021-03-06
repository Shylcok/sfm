#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license:
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: order_service.py
@time: 16/10/14 下午8:03
"""

from base_service import BaseService
import logging
from tornado.gen import coroutine
from tornado import gen
from constant import *
import json
from utility.common import Common
import contextlib
from tornado.gen import Return
import traceback


class CommitOrderError(Exception):
    def __init__(self, value):
        self.message = value

    def __str__(self):
        return self.message


class HandleStockError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class OrderGenerator(BaseService):
    def __init__(self, user_id):
        self.order_id = GENERATOR_ORDER_ID(user_id)
        self.order_sku_count = 0  # 商品数量
        self.order_sku_amount = 0  # 订单商品价格 200
        self.credit_amount = 0  # 额度卡-10
        self.ship_amount = CONST_ORDER_SHIP_AMOUNT  # 运费10
        self.pay_amount = 0  # 支付价格
        self.order_sku_infos = []
        self.order_info = {}

    def __str__(self):
        return json.dumps(self, default=lambda obj: obj.__dict__)

    @coroutine
    def add_sku_list(self, sku_list):
        for sku in sku_list:
            sku_id = sku['sku_id']
            sku_count = sku['sku_count']
            first_price = sku['first_price']
            sku_info = yield self.context_repos.expernal_repo.get_sku_info(sku_id)
            if sku_info:
                """打开首付验证"""
                if int(sku['first_price']) < int(sku_info['firstPay'][-1]):
                    logging.error(
                        '首付价格低于最低首付, first_price=%s, firstPay=%s' % (sku['first_price'], sku_info['firstPay']))
                    raise gen.Return(False)
                sku_info['order_sku_id'] = sku_id
                sku_info['order_sku_count'] = sku_count
                sku_info['order_first_price'] = first_price
                # sku_info['order_credit_price'] = int(sku_info['realPrice']) - first_price

                ship_amount = int(sku_info['postfee'])
                sku_amount = sku_count * int(sku_info['realPrice'])
                first_amount = sku_count * sku_info['order_first_price']
                credit_amount = sku_amount - first_amount

                self.order_sku_count += sku_count  # 商品价格
                self.order_sku_amount += sku_amount  # 商品数量
                self.credit_amount -= credit_amount  # 购物卡价格
                self.ship_amount += ship_amount

                self.pay_amount = self.order_sku_amount + self.credit_amount + self.ship_amount
                self.order_sku_infos.append(sku_info)
            else:
                logging.error('不存在的商品, sku_id=%s' % sku_id)
                raise gen.Return(False)

    @coroutine
    def add_cart_list(self, cart_list):
        for cart in cart_list:
            cart_id = int(cart['cart_id'])
            cart_info = yield self.context_repos.cart_repo.select_by_id(cart_id)
            if cart_info is None:
                logging.error('传入不存在的购物车id:%s' % cart_id)
                raise gen.Return(False)
            else:
                sku_id = cart_info['sku_id']
                sku_count = cart_info['sku_count']
                first_price = int(cart['first_price'])
                sku_info = yield self.context_repos.expernal_repo.get_sku_info(sku_id)
                if sku_info:
                    """打开首付验证"""
                    if int(cart['first_price']) < int(sku_info['firstPay'][-1]):
                        logging.error('首付价格低于最低首付, first_price=%s, firstPay=%s' % (
                            cart['first_price'], sku_info['firstPay']))
                        raise gen.Return(False)
                    sku_info['order_sku_id'] = sku_id
                    sku_info['order_sku_count'] = sku_count
                    sku_info['order_first_price'] = first_price
                    # sku_info['order_credit_price'] = int(sku_info['realPrice']) - first_price

                    sku_amount = sku_count * int(sku_info['realPrice'])
                    first_amount = sku_count * sku_info['order_first_price']
                    credit_amount = sku_amount - first_amount

                    ship_amount = int(sku_info['postfee'])
                    self.order_sku_count += sku_count  # 商品价格
                    self.order_sku_amount += sku_amount  # 商品数量
                    self.credit_amount -= credit_amount  # 购物卡价格
                    self.ship_amount += ship_amount

                    self.pay_amount = self.order_sku_amount + self.credit_amount + self.ship_amount
                    self.order_sku_infos.append(sku_info)
                else:
                    logging.error('不存在的商品, sku_id=%s' % sku_id)
                    raise gen.Return(False)

    def get(self):
        self.order_info = {
            'order_sku_infos': self.order_sku_infos,
            'order_sku_count': self.order_sku_count,
            'order_sku_amount': self.order_sku_amount,
            'credit_amount': self.credit_amount,
            'ship_amount': self.ship_amount,
            'pay_amount': self.pay_amount
        }
        return self.order_info


class OrderService(BaseService):
    def __init__(self, services):
        super(OrderService, self).__init__(services)

    @contextlib.contextmanager
    def make_content_stock(self, order_info):
        f = self.decrease_stocks(order_info)
        is_success = f.result()
        if is_success is False:
            raise HandleStockError('锁库存失败')
        try:

            yield {}

        except Exception, err:
            logging.error('订单提交失败:%s, 解库存' % err)
            f = self.increase_stocks(order_info.order_id)
            is_success = f.result()
            if is_success is False:
                logging.error('解库存失败, order_id=%s' % order_info.order_id)
            else:
                raise err

    def get_address(self, user_id):
        res = self.context_repos.address_repo.select_by_user_id(user_id)
        return res

    def add_address(self, user_id, address_info):
        name = address_info['name']
        mobile = address_info['mobile']
        address = address_info['address']
        is_default = address_info['is_default']
        if is_default == 1:
            self.context_repos.address_repo.update_by_user_id_set_no_default(user_id)

        res = self.context_repos.address_repo.insert(user_id, name, mobile, address, is_default)
        return {'code': 0, 'msg': '添加地址成功', 'data': res}

    def update_address(self, id, user_id, address_info):
        name = address_info['name']
        mobile = address_info['mobile']
        address = address_info['address']
        is_default = address_info['is_default']
        if is_default == 1:
            self.context_repos.address_repo.update_by_user_id_set_no_default(user_id)

        res = self.context_repos.address_repo.update_by_id(user_id, name, mobile, address, is_default, id)
        return {'code': 0, 'msg': '更新地址成功', 'data': res}

    def delete_address(self, id):
        res = self.context_repos.address_repo.delete_by_id(id)
        return {'code': 0, 'msg': '删除地址成功', 'data': res}

    def set_default(self, user_id, id):
        self.context_repos.address_repo.update_by_user_id_set_no_default(user_id)
        res = self.context_repos.address_repo.update_by_id_set_default(id)
        return {'code': 0, 'msg': '设置默认地址成功', 'data': res}

    @coroutine
    def prepare_order(self, user_id, order_type, cart_list, sku_list, coupon_code):
        # 计算出首付价格, 额度卡透资价格, 运费, 需要支付的价格
        order_info = OrderGenerator(user_id)

        if order_type == 'cart':
            yield order_info.add_cart_list(cart_list)
        elif order_type == 'sku':
            yield order_info.add_sku_list(sku_list)

        res = order_info.get()
        raise gen.Return(res)

    @coroutine
    def decrease_stocks(self, order_info):
        """
        锁库存
        :param order_info:
        :return:
        """
        success_decrease_sku_infos = []
        for sku in order_info.order_sku_infos:
            sku_id = sku['order_sku_id']
            sku_count = sku['order_sku_count']
            success = yield self.context_repos.expernal_repo.decrease_stock(sku_id, sku_count)
            if success is True:
                logging.info('锁库存成功, sku_id=%s, sku_count=%s' % (sku_id, sku_count))
                success_decrease_sku_infos.append({'sku_id': sku_id, 'sku_count': sku_count})
            else:
                logging.error('锁库存失败, 解锁之前锁定的库存')
                for decrease_sku in success_decrease_sku_infos:
                    s_id = decrease_sku['sku_id']
                    s_count = decrease_sku['sku_count']
                    res = yield self.context_repos.expernal_repo.increase_stock(s_id, s_count)
                    if res is True:
                        logging.info('解锁库存成功 sku_id=%s, sku_count=%s' % (s_id, s_count))
                    else:
                        logging.error('解锁库存失败 sku_id=%s, sku_count=%s' % (s_id, s_count))
                raise gen.Return(False)

        raise gen.Return(True)

    @coroutine
    def increase_stocks(self, order_id):
        """
        解库存
        :param order_id:
        :return:
        """
        order_info = self.context_repos.order_mongodb.find_one({"_id": order_id})
        for sku_info in order_info['order_sku_infos']:
            sku_id = sku_info['order_sku_id']
            sku_count = sku_info['order_sku_count']
            success = yield self.context_repos.expernal_repo.increase_stock(sku_id, sku_count)
            if success:
                logging.info('解锁库存成功, sku_id=%s, sku_count=%s' % (sku_id, sku_count))
            else:
                logging.error('解锁库存失败, sku_id=%s, sku_count=%s' % (sku_id, sku_count))
                raise Return(False)

        raise Return(True)

    @coroutine
    def _commit_order(self, order_info, user_id, address_id, user_note):
        with self.make_content_stock(order_info) as stock:
            """订单详细数据 入库, mongodb 和 mysql"""
            order_info_json = str(order_info)
            order_info_dict = json.loads(order_info_json)
            order_info_dict['_id'] = order_info.order_id
            # 此处选择mongodb 做备份存储,其实完全没有必要, 我们可以认为订单锁库存后一定会入库成功, 子订单也一定会入库成功, 解锁库存应该从mysql的子订单中查找
            self.context_repos.order_mongodb.insert_one(order_info_dict)
            # card_id = self.context_repos.credit_card_repo.select(user_id)

            """判断额度卡是否足够"""
            card_info = self.context_repos.credit_card_repo.select(user_id)
            remain_amount = card_info['remain_amount']
            if remain_amount + order_info.credit_amount < 0:
                logging.warn('额度卡余额不足, remain_amount=%s, credit_amount=%s' % (remain_amount, order_info.credit_amount))
                # raise gen.Return({'code': 310, 'msg': '额度卡余额不足, remain_amount=%s, credit_amount=%s' % (
                #     remain_amount, order_info.credit_amount)})
                raise CommitOrderError(
                    '额度卡余额不足, remain_amount=%s, credit_amount=%s' % (remain_amount, order_info.credit_amount))

            """订单数据如数据库"""
            last_rowid = self.context_repos.order_repo.insert(order_info.order_id, order_info.ship_amount,
                                                              order_info.order_sku_amount, order_info.credit_amount,
                                                              order_info.pay_amount, order_info.order_sku_count,
                                                              user_id,
                                                              address_id, user_note, card_info['card_id'])
            if last_rowid < 0:
                """订单插入失败,解库存"""
                # yield self.increase_stocks(order_info.order_id)
                logging.error('订单提交失败, 订单数据插入数据库错误:')
                logging.error(order_info.get())
                # raise gen.Return({'code': 111, 'msg': '订单提交失败, 订单数据生成错误'})
                raise CommitOrderError('订单提交失败, 订单数据插入数据库错误')

            else:
                """ 订单生产成功"""
                logging.info('订单数据库中生成 order_id=%s, 进入过期消息队列' % order_info.order_id)
                self.services.order_overtime_task_service.commit_order_celery(order_info.order_id)

            """更新订单子表, 和mongodb冗余"""
            for order_sku_info in order_info.order_sku_infos:
                sku_id = order_sku_info['skuid']
                sku_count = order_sku_info['order_sku_count']
                sku_weight = order_sku_info['weight']
                sku_amount = int(order_sku_info['realPrice'])
                sku_name = order_sku_info['name']
                sku_image_url = order_sku_info['imglist'][0] if (len(order_sku_info['imglist']) > 0) else ''
                first_price = order_sku_info['order_first_price']

                self.context_repos.sku_order_repo.insert(order_info.order_id, sku_id, sku_count, sku_weight, sku_amount,
                                                         sku_name,
                                                         sku_image_url, first_price)

            logging.info('订单提交成功,单号:%s' % order_info.order_id)

    @coroutine
    def commit_order(self, user_id, address_id, order_type, cart_list, sku_list, user_note, coupon_code):
        """
        提交生成订单
        :param user_id:
        :param address_id:
        :param order_type:
        :param cart_list:
        :param sku_list:
        :param user_note:
        :param coupon_code:
        :return:
        """

        """生成虚拟订单"""
        order_info = OrderGenerator(user_id)
        if order_type == 'cart':
            success = yield order_info.add_cart_list(cart_list)
            if success is False:
                raise gen.Return({'code': 210, 'msg': '异常数据'})

        elif order_type == 'sku':
            success = yield order_info.add_sku_list(sku_list)
            if success is False:
                raise gen.Return({'code': 210, 'msg': '异常数据'})
        #
        # """提交订单之前锁库存"""
        # success_descrase_stock = yield self.decrease_stocks(order_info)
        # if success_descrase_stock is False:
        #     raise gen.Return(False)
        # else:
        #     logging.info('锁库存全部成功, 订单准备插入数据库 order_id=%s' % order_info.order_id)
        try:
            res = yield self._commit_order(order_info, user_id, address_id, user_note)
            if res is False:
                res
        except Exception, err:
            logging.error('提交订单操作失败:%s' % err)
            traceback.print_exc()
            raise gen.Return({'code': 271, 'msg': '提交订单操作失败:%s' % err})

        """如果来自购物车,设置购物车中的status=0"""
        if order_type == "cart":
            for card_info in cart_list:
                logging.info('提交订单,删除购物车内数据, cart_id=%s' % str(card_info))
                self.context_repos.cart_repo.delete_by_cart_id(card_info['cart_id'])

        raise gen.Return({'code': 0, 'msg': '订单提交成功', 'data': order_info.order_id})

    @coroutine
    def get_order_list(self, user_id, order_type, page, count):
        """
        获取我的订单列表
        :param count:
        :param page:
        :param order_type:
        :param user_id:
        :return:
        """
        if order_type == 'all':
            res, total = yield self.context_repos.order_repo.select_by_user_id_all(user_id, page, count)
        elif order_type == 'need_pay':
            res, total = yield self.context_repos.order_repo.select_by_user_id_state(user_id, 0, page, count)
        elif order_type == 'need_send':
            res, total = yield self.context_repos.order_repo.select_by_user_id_state(user_id, 1, page, count)
        elif order_type == 'need_receive':
            res, total = yield self.context_repos.order_repo.select_by_user_id_state(user_id, 2, page, count)
        elif order_type == 'complete':
            res, total = yield self.context_repos.order_repo.select_by_user_id_state(user_id, 3, page, count)
        elif order_type == 'cancel':
            res, total = yield self.context_repos.order_repo.select_by_user_id_state(user_id, 4, page, count)
        elif order_type == 'overtime':
            res, total = yield self.context_repos.order_repo.select_by_user_id_state(user_id, 5, page, count)
        else:
            raise gen.Return({'code': 201, 'msg': 'type参数错误'})
        for order in res:
            order_id = order['order_id']
            sku_orders = yield self.context_repos.sku_order_repo.select_by_order_id(order_id)
            order['skus_info'] = sku_orders

        pagination = Common().pagination(total, page, count)
        raise gen.Return({'code': 0, 'msg': '获取成功', 'data': {'pagination': pagination, 'order_list': res}})

    @coroutine
    def get_order_brief_for_pay(self, user_id, order_id):
        """
        支付前的订单简讯
        :param user_id:
        :param order_id:
        :return:
        """
        order_info = yield self.context_repos.order_repo.select_for_pay(user_id, order_id)
        if order_info is None:
            logging.error('订单错误 id=%s, user_id=%s' % (order_id, user_id))
            raise gen.Return({'code': 134, 'msg': '订单错误'})
        else:
            address_info = yield self.context_repos.address_repo.select_by_id(order_info['address_id'])
            res = {'address_info': address_info,
                   'order_id': order_info['order_id'],
                   'sku_infos': []
                   }
            skus = yield self.context_repos.sku_order_repo.select_by_order_id(order_id)
            for sku in skus:
                res['sku_infos'].append({'sku_name': sku['sku_name'], 'sku_id': sku['sku_id']})

            res['pay_amount'] = order_info['pay_amount']
            raise gen.Return(res)

    @coroutine
    def delete_order(self, user_id, order_id):
        res = yield self.context_repos.order_repo.delete_order(user_id, order_id)
        raise gen.Return(res)

    @coroutine
    def confirm_order(self, user_id, order_id):
        res = yield self.context_repos.order_repo.update_state_3(user_id, order_id)
        if res > 0:
            raise gen.Return({'code': 0, 'msg': '订单确认成功'})
        else:
            logging.error('订单状态错误,订单确认失败, order_id=%s' % order_id)
            raise gen.Return({'code': 211, 'msg': '卖家可能还未发货,订单确认失败'})

    @coroutine
    def cancel_order(self, user_id, order_id, reason):
        res = yield self.context_repos.order_repo.update_state_4(user_id, order_id, reason)
        if res > 0:
            raise gen.Return({'code': 0, 'msg': '订单取消成功'})
        else:
            logging.error('订单状态不正确,订单取消失败, order_id=%s' % order_id)
            raise gen.Return({'code': 212, 'msg': '订单状态不正确,订单取消失败'})

    @coroutine
    def get_order(self, order_id):
        order_info = yield self.context_repos.order_repo.select_by_order_id(order_id)
        order_sku_infos = yield self.context_repos.sku_order_repo.select_by_order_id(order_id)
        if order_sku_infos is None or order_info is None:
            raise gen.Return({'code': 218, 'msg': '订单%s不存在' % order_id})
        order_info['skus_info'] = order_sku_infos
        address_info = yield self.context_repos.address_repo.select_by_id(order_info['address_id'])
        order_info['address_info'] = address_info

        res = {'order_info': order_info}

        raise gen.Return({'code': 0, 'msg': '获取成功', 'data': res})

    """--------------后端服务——————————————————————————"""

    @coroutine
    def send_out(self, order_id, logistics_id, logistics):
        res = yield self.context_repos.order_repo.update_state_2(order_id, logistics_id, logistics)
        if res > 0:
            raise gen.Return({'code': 0, 'msg': '确认发货'})
        else:
            raise gen.Return({'code': 510, 'msg': '确认发货失败'})

    @coroutine
    def get_list(self, u_id, u_mobile, order_id, ctime_st, ctime_ed, order_type, page, count):
        if order_type == 'all':
            orders, total = yield self.context_repos.order_repo.select_for_background_all(u_id, u_mobile, order_id,
                                                                                          ctime_st, ctime_ed, page,
                                                                                          count)
        else:
            if order_type == 'need_pay':
                state = 0
            elif order_type == 'need_send':
                state = 1
            elif order_type == 'need_receive':
                state = 2
            elif order_type == 'complete':
                state = 3
            elif order_type == 'cancel':
                state = 4
            elif order_type == 'overtime':
                state = 5
            orders, total = yield self.context_repos.order_repo.select_for_background(u_id, u_mobile, order_id, state,
                                                                                      ctime_st, ctime_ed, page, count)

        res = {'orders': orders, 'pagination': Common().pagination(total, page, count)}
        raise gen.Return(res)

    @coroutine
    def get_detail(self, order_id):
        order_info = yield self.context_repos.order_repo.select_by_order_id(order_id)
        user_id = order_info['user_id']
        user_info = self.context_repos.user_repo.select_by_user_id(user_id)
        address_id = order_info['address_id']
        address_info = yield self.context_repos.address_repo.select_by_id(address_id)
        sku_infos = yield self.context_repos.sku_order_repo.select_by_order_id(order_id)
        pay_info = self.context_repos.pay_repo.select_order_id(order_id)
        order_log_infos = self.context_repos.operate_log_repo.select_by_target_id(order_id)

        res = {'order_info': order_info,
               'user_info': user_info,
               'address_info': address_info,
               'sku_infos': sku_infos,
               'pay_info': pay_info,
               'order_log_infos': order_log_infos
               }
        raise Return(res)

    @coroutine
    def add_admin_note(self, order_id, admin_note):
        res = yield self.context_repos.order_repo.add_admin_note(order_id, admin_note)
        raise Return(res)


if __name__ == "__main__":
    order = OrderGenerator('111')
    order.order_sku_infos = [{'sku_id': 100, "sku_count": 1}]
    print str(order)
