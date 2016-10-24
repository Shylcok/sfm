#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: user_handler.py
@time: 16/10/13 下午2:01
"""

from handler.base_handler import BaseHandler
from core.handler_decorator import handler_decorator
import random
import time
from settings import *


class UserHandler(BaseHandler):
    @handler_decorator(perm=1, types={'user_id': str}, plain=False, async=False, finished=True)
    def get_user_info(self, user_id):
        user = self.context_services.user_service.get_user_info(user_id)
        return user

    @handler_decorator(perm=0, types={'mobile': str}, plain=False, async=False, finished=True)
    def send_verify_code(self, mobile):
        """
        发送短信验证码
        :param mobile:
        :return:
        """
        chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        x = random.choice(chars), random.choice(chars), random.choice(chars), random.choice(chars)
        verifyCode = "".join(x)
        self.set_cookie('sfm_sms_verify', verifyCode, httponly=True, expires=time.time() + 60 * 15)
        res = self.context_services.user_service.send_tel_msg(verifyCode, mobile)
        return res

    @handler_decorator(perm=0, types={'mobile': str, 'pwd': str}, plain=False, async=False, finished=True)
    def register(self, mobile, pwd):
        """
        注册
        :param mobile:
        :param pwd:
        :return:
        """
        res = self.context_services.user_service.register(mobile, pwd)
        return res

    @handler_decorator(perm=0, types={'mobile_user_name': str, 'pwd': str}, plain=False, async=False, finished=True)
    def login(self, mobile_uer_name, pwd):
        """
        登录
        :param mobile:
        :param pwd:
        :return:
        """
        res, user_token = self.context_services.user_service.login(mobile_uer_name, pwd)
        if res['code'] == 0:
            self.set_cookie('sfm_user_token', user_token, httponly=True,
                            expires=time.time() + 60 * 60)  # 安全cookie 60分钟, js 无法获取该cookie

        return res

    @handler_decorator(perm=0, types={}, plain=False, async=False, finished=True)
    def logout(self):
        """
        退出
        :return:
        """
        self.clear_cookie('sfm_user_token')
        return {'code': 0, 'msg': '注销成功'}

    @handler_decorator(perm=1, types={'user_id': str, 'old_pwd': str, }, plain=False, async=False, finished=True)
    def modify_pwd(self, user_id, old_pwd, new_pwd):
        """
        修改密码
        :param user_id:
        :param old_pwd:
        :param new_pwd:
        :return:
        """
        res = self.context_services.user_service.modify_pwd(user_id, old_pwd, new_pwd)
        if res['code'] == 0:
            self.logout()
        return res

    @handler_decorator(perm=1, types={'user_id': str, 'new_user_name': str,}, plain=False, async=False, finished=True)
    def modify_user_name(self, user_id, new_user_name):
        """
        修改用户名
        :param user_id:
        :param new_user_name:
        :return:
        """
        res = self.context_services.user_service.modify_user_name(user_id, new_user_name)
        return res
