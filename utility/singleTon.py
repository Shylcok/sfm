# -*- coding: utf-8 -*-
"""
Created on 2016年3月25日

@des:
 for signel class
@author:55Haitao
"""


def SingleTon(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton
