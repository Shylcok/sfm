# -*- coding: utf-8 -*-
'''
Created on 2016锟斤拷4锟斤拷15锟斤拷

@author: 55Haitao
'''
from utility.logTool import HT_ERROR, HT_LOG


def DaoRetry(func):
    def __daoRetry(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception, e:
            if "MySQL server has gone away" in str(e):
                HT_ERROR(e.message)
                HT_LOG("we try it again")
                return func(*args, **kwargs)
            else:
                raise e
        
    return __daoRetry
                    
    
    
    
    
    
    
        
