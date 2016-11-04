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

from celery import Celery
from service.order_overtime_task_service import OrderOvertimeTaskService

celery = Celery('tasks', broker='redis://127.0.0.1:6379/0')
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

orderOverTime = OrderOvertimeTaskService()


@celery.task(bind=True, max_retries=10,
             default_retry_delay=1 * 6)  # bind 表示开启, max_retries 是重新尝试的次数,default_retry_delay 是默认的间隔时间，尝试的时间
def exec_task_order_overtime(self, order_id):  # 订单到期后,执行订单失效的任务
    try:
        logger.info('exec_task_order_overtime order_id=%s' % order_id)
        orderOverTime.process_over_time(order_id)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=3)  # 3 秒后继续尝试
