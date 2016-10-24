# -*- coding: utf-8 -*-
"""
Created on 2016年3月14日

@author:
"""

from utility import logging
from utility.logging import handlers
from utility.myConfig import MyConfig
from utility.singleTon import SingleTon
from utility.common import Common
import datetime





@SingleTon
class LogTool(object):
    def __init__(self):
        # 创建一个logger
        self.logger = logging.getLogger(MyConfig().logModule)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        Common().createDir(MyConfig().logPath)
        fh = logging.handlers.RotatingFileHandler(MyConfig().logPath + MyConfig().logModule + '.log', maxBytes=20*1024*1024, backupCount=10)
        #FileHandler()
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台,可以不需要
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        #2011-08-31 19:18:29,816 - mylogger - INFO - start ok!
        formatter = logging.Formatter('%(asctime)s-%(filename)s:%(lineno)s-%(name)s-%(levelname)s-%(message)s')
        fh.setFormatter(formatter)
        
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        # 记录一条日志
        self.logger.info('Init Logger OK !')



def HT_LOG(msg):
    LogTool().logger.info(msg)

def HT_WARN(msg):
    LogTool().logger.warn(msg)
    
def HT_ERROR(msg):
    LogTool().logger.error(msg)

def HT_EXCEPT(msg):
    LogTool().logger.exception(msg)


def HT_FUNC_DECO(fun):
    def __deco(*args, **kwargs):
        if args is not None:
            self = args[0]

        msg = "==>" + self.__class__.__name__ + ":" + fun.__name__
        LogTool().logger.info(msg)
        
        ret = fun(*args, **kwargs)

        msg = "<==" + self.__class__.__name__ + ":" + fun.__name__
        LogTool().logger.info(msg)
        return ret
    return __deco

if __name__ == "__main__":
    HT_ERROR('123')
