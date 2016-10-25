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
import time
from settings import *
import constant


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
        res = self.context_services.user_service.send_verify_code(mobile)
        return res

    @handler_decorator(perm=0, types={'mobile': str, 'pwd': str, 'sms_verify': str}, plain=False, async=False,
                       finished=True)
    def signup(self, mobile, pwd, sms_verify):
        """
        注册
        :param mobile:
        :param pwd:
        :return:
        """
        res = self.context_services.user_service.signup(mobile, pwd, sms_verify)
        if res['code'] == 0:
            res = self.signin(mobile, pwd)

        return res

    @handler_decorator(perm=0, types={'mobile_user_name': str, 'pwd': str}, plain=False, async=False, finished=True)
    def signin(self, mobile_uer_name, pwd):
        """
        登录
        :param mobile_uer_name:
        :param pwd:
        :return:
        """
        res, user_token = self.context_services.user_service.signin(mobile_uer_name, pwd)
        if res['code'] == 0:
            self.set_cookie(constant.CONST_COOKIE_USER_TOKEN_NAME, user_token, httponly=True,
                            expires=time.time() + constant.CONST_COOKIE_EXPIRES)  # 安全cookie 60分钟, js 无法获取该cookie
            self.set_cookie(constant.CONST_COOKIE_USER_NAME, res['user_name'],
                            expires=time.time() + constant.CONST_COOKIE_EXPIRES)

        return res

    @handler_decorator(perm=0, types={}, plain=False, async=False, finished=True)
    def signout(self):
        """
        退出
        :return:
        """
        self.clear_cookie('sfm_user_token')
        return {'code': 0, 'msg': '注销成功'}

    @handler_decorator(perm=1, types={'user_id': str, 'old_pwd': str,}, plain=False, async=False, finished=True)
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
