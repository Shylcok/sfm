# -*- coding: utf-8 -*-
'''
Created on 2016年5月17日

@author: 55Haitao
'''

import urllib
import urllib2

from utility.singleTon import SingleTon

@SingleTon
class UrlRequest(object):
    def __init__(self):
        pass
    
    def get(self, url):
        req = urllib2.Request(url)        
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        return res