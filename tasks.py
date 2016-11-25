#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: tasks.py
@time: 16/11/4 下午4:16
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from celery import Celery
from handler.base_handler import BaseHandler
from tornado.gen import Return
from tornado.ioloop import IOLoop

celery = Celery('tasks', broker='redis://127.0.0.1:6379/0')
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery.task(bind=True, max_retries=10,
             default_retry_delay=1 * 6)  # bind 表示开启, max_retries 是重新尝试的次数,default_retry_delay 是默认的间隔时间，尝试的时间
def exec_task_order_overtime(self, order_id):  # 订单到期后,执行订单失效的任务
    try:
        logger.info('===================> exec_task_order_overtime order_id=%s' % order_id)
        # IOLoop.current().run_sync(lambda: BaseHandler.context_services.order_overtime_task_service.process_over_time(order_id))
        f = BaseHandler.context_services.order_overtime_task_service.process_over_time(order_id)
        success = f.result()
        # while True:
        #     try:
        #         success.next()
        #     except Exception, e:
        #         logger.warn('success.next over: %s' % e.message)
        #         break
        # success = True
        logger.info('process result: %s' % success)
        if success is False:
            logger.error(
                '<================order_overtime_task_service.process_over_time Failed, order_id=%s' % order_id)
            raise Return(False)
        else:
            logger.info(
                '<=================order_overtime_task_service.process_over_time Success, order_id=%s' % order_id)
    except Exception as exc:
        logger.info('exec_task_order_overtime retry, order_id=%s' % order_id)
        raise self.retry(exc=exc, countdown=3)  # 3 秒后继续尝试


@celery.task(bind=True, max_retries=10,
             default_retry_delay=1 * 6)  # bind 表示开启, max_retries 是重新尝试的次数,default_retry_delay 是默认的间隔时间，尝试的时间
def exec_task_card_borrow(self, order_id):  # 订单到期后,执行订单失效的任务
    try:
        logger.info('===================> exec_task_card_borrow order_id=%s' % order_id)
        # IOLoop.current().run_sync(
        #     lambda: BaseHandler.context_services.order_overtime_task_service.process_over_time(order_id))
        # success = BaseHandler.context_services.order_overtime_task_service.process_over_time(order_id)
        # while True:
        #     try:
        #         success.next()
        #     except Exception, e:
        #         logger.warn('success.next over: %s' % e.message)
        #         break
        f = BaseHandler.context_services.order_overtime_task_service.process_remind_card_notify(order_id)
        success = f.result()
        logger.info('process result: %s' % success)
        if success is False:
            logger.error(
                '<================exec_task_card_borrow.process_remind_card_notify Failed, order_id=%s' % order_id)
            raise Return(False)
        else:
            logger.info(
                '<=================exec_task_card_borrow.process_remind_card_notify Success, order_id=%s' % order_id)
    except Exception as exc:
        logger.info('exec_task_card_borrow retry, order_id=%s' % order_id)
        raise self.retry(exc=exc, countdown=3)  # 3 秒后继续尝试



                # if __name__ == "__main__":
#     exec_task_order_overtime(1, 110)