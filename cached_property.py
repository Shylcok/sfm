#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: suyuan
@license: 
@contact: suyuan@gmail.com
@site: https://github.com/su6838354/sfm
@software: PyCharm
@file: cached_property.py
@time: 16/11/2 上午11:30
"""



class _Missing(object):
    def __repr__(self):
        return 'no value'

    def __reduce__(self):
        return '_missing'


_missing = _Missing()


class cached_property(object):
    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func


    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        value = instance.__dict__.get(self.__name__, _missing)
        if value is _missing:
            value = self.func(instance)
            instance.__dict__[self.__name__] = value
        return value

class Foo(object):

    @cached_property
    def foo(self):
        print 'first calculate'
        result = 'this is result'
        return result



f = Foo()

print f.foo
print f.foo