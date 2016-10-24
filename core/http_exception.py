#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: http_exception.py
@time: 16/10/12 下午1:54
"""
import json

class CoreException(Exception):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return self.msg


class Http(Exception):
    def __init__(self, status_code, code, msg, data=None):
        # type: (object, object, object) -> object
        self.status_code = status_code # http 状态码
        self.code = code # 接口定义的返回状态
        self.msg = msg
        self.data = data

    def convert_to_dict(self):
        """把Object对象转换成Dict对象"""
        dict = {}
        dict.update(self.__dict__)
        return dict

    def __str__(self):
        # res = {'code': self.code, 'sys': self.sys, 'emsg': self.emsg, }
        dict = self.convert_to_dict()
        return json.dumps(dict)



def Http200(data):
    if 'code' in data:
        code = data['code']
        msg = data['msg']
        data.pop('code')
        data.pop('msg')
    else:
        code = 0
        msg = u'http请求成功'

    if 'status_code' in data:
        status_code = data['status_code']
    else:
        status_code = 200

    return Http(status_code, code, msg,  data)


def Http400(data):
    return Http(400, 400, u'(错误请求)服务器不理解请求的语法', data)

def Http401(data):
    return Http(401, 401, u'(未授权)请求要求身份验证。 对于需要登录的网页，服务器可能返回此响应。', data)

def Http403(data):
    return Http(403, 403, u'(禁止)服务器拒绝请求。', data)

def Http404(data):
    return Http(404, 404, u'(未找到)服务器找不到请求的网页。', data)



E_CORE_MISSING_ARGUMENT = 100
E_CORE_INVALID_ARGUMENT = 101
E_CORE_INTERNAL_EXCEPTION = 102
