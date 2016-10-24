#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: handler_decorator.py
@time: 16/10/13 上午9:47
"""

import inspect


def inspect_func(func):
    rest_spec = {
        'module': inspect.getmodule(func).__name__,
        'name': func.func_name,
        'doc': func.__doc__,
        'params': []
    }

    argspec = inspect.getargspec(func)
    rest_spec['args'] = argspec.varargs  # 没有用处
    rest_spec['kwargs'] = argspec.keywords  # 没有用处

    arg_index = 0
    default_count = len(argspec.defaults) if argspec.defaults else 0
    default_start = len(argspec.args) - default_count  # 默认值开始位置

    for item in argspec.args:
        if arg_index >= default_start:
            default_value = argspec.defaults[arg_index - default_start]
            required = False
        else:
            default_value = None
            required = True

        rest_spec['params'].append(
            {
                'name': item,
                'required': required,
                'default': default_value,
                'type': str
            }
        )
        arg_index += 1

    return rest_spec


'''如果指定了权限，则方法必须接受一个uid参数，该参数是登陆用户的ID'''


def handler_decorator(perm=None, types=None, plain=False, async=False, finished=True):
    def wrapper(func):
        rest_spec = inspect_func(func)
        rest_spec['perm'] = perm
        rest_spec['plain'] = plain
        rest_spec['async'] = async
        rest_spec['finished'] = finished

        if types:
            for item in rest_spec['params']:
                if item['name'] in types:
                    item['type'] = types[item['name']]  # 更新参数类型

        func.rest_spec = rest_spec
        return func

    return wrapper
