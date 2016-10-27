#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: base_handler_bak.py
@time: 16/9/27 下午7:52
"""

import tornado.web
import tornado.gen
import json
import logging
from core.http_exception import *
from service.user_service import UserService
import constant


class CoreHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(CoreHandler, self).__init__(application, request, **kwargs)

    def _check_perm(self, perm):
        if perm == 0:  # 不需要权限
            return True
        else:
            return False

    def _set_cors(self):
        """
        设置跨域
        :return:
        """
        if 'Origin' in self.request.headers:
            host = self.request.headers['Origin']
        else:
            host = '*'
        self.set_header('Access-Control-Allow-Origin', host)
        self.set_header('Access-Control-Allow-Credentials', 'true')  # 跨子域名访问
        self.set_header('Access-Control-Allow-Methods', 'POST')
        self.set_header('Access-Control-Allow-Headers',
                        'X-Requested-With, Content-Type')
        self.set_header('Content-Type', 'application/json;charset=utf-8')

    def finish(self, http):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.set_header('Server', 'sfm')
        if isinstance(http, Http):
            self.set_status(http.status_code)
        res = str(http)
        self._set_cors()
        super(CoreHandler, self).finish(res)

    def set_cookie(self, name, value, domain=None, expires=None, path="/",
                   expires_days=None, **kwargs):
        host = self.request.headers['Origin']
        domain = host[11:18]  # 临时设置cookie作用域名
        return super(CoreHandler, self).set_cookie(name, value, domain, expires, path,
                                                   expires_days, **kwargs)

    def options(self, *args, **kwargs):
        self.finish('')

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self.__handle(*args, **kwargs)

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        yield self.__handle(*args, **kwargs)

    @tornado.gen.coroutine
    def __handle(self, *args, **kwargs):
        request = self.request
        url = request.path.split('/')
        module_name = url[-2]
        method_name = url[-1]

        func = getattr(self, method_name, None)  # 得到该对象的成员函数
        if not func:
            self.finish(Http404('路由不存在'))
            # raise tornado.gen.Return()
            return

        request_data = {}  # 参数梳洗
        """post arguments"""
        if (request.method == 'POST' and
                    'application/json' in request.headers.get('Content-Type')):
            try:
                body_dic = json.loads(request.body)
            except ValueError, e:
                self.finish(Http400('传入的参数不匹配合法的json字符串'))
                return
            request_data.update(body_dic)
        elif request.body_arguments:
            request_data.update(request.body_arguments)
        """url arguments reconstruct"""
        query_arguments = dict(request.query_arguments)
        for k, v in query_arguments.items():
            if type(v) is list and len(v) == 1:
                query_arguments[k] = v[0]
        request_data.update(query_arguments)
        """公共参数"""
        request_data.update({'client_ip': self.request.remote_ip})
        rest_spec = func.rest_spec  # 获取方法的装饰器参数

        """权限验证"""
        if self._check_perm(rest_spec['perm']) is False:  # 接口没有开发权限
            # 接口需要用户权限
            sfm_user_token = self.get_cookie(constant.CONST_COOKIE_USER_TOKEN_NAME)
            user_token_dic = UserService._decrypt(sfm_user_token)
            if not user_token_dic:
                self.finish(Http401('未登录'))
                return
            request_data['user_id'] = user_token_dic['user_id']
            request_data['mobile'] = user_token_dic['mobile']
            request_data['user_name'] = user_token_dic['user_name']

        params = {}
        """组装参数params"""
        for item in rest_spec['params']:
            name, required, default = item['name'], item['required'], item['default']
            if name == 'self':
                continue
            elif name in request_data:
                params[name] = request_data[name]
            elif not required:
                params[name] = default
            else:
                self.finish(Http400('缺少参数%s' % name))
                return

            # 参数类型转换
            value = params[name]
            # if item['type'] in (dict, list, tuple):
            #     value = json.loads(value)

            if type(value) is not item['type']:
                value = item['type'](value)

            params[name] = value

        """执行"""
        if rest_spec['async']:
            result = yield func(**params)
        else:
            result = func(**params)

        if rest_spec['finished'] is True:
            if rest_spec['plain'] is False:
                self.finish(Http200(result))  # 返回规格结果
                return
            else:
                super(CoreHandler, self).finish(result)  # 返回原始结果
                return
