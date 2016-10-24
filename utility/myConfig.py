# -*- coding: utf-8 -*-
"""
Created on 2016年3月21日
Modify on 2016年3月25日

@des

@author:55Haitao
"""
import sys
import os
from utility.singleTon import SingleTon
from utility.common import Common

ENV = os.getenv('MALL_ENV')
"""
设置用户级别的环境变量
vi ~/.bashrc
export SFM_ENV="DEV"
souce ~/.bashrc
"""

@SingleTon 
class MyConfig(object):
    def __init__(self):
        if ENV == "DEV":
            self.debug = True
        else:
            self.debug = False
        
        self.sqlUsr = "55cateoptsys"
        self.sqlPasswd = "55haitao"
        self.sqlDataBase = "cateOptSys"            

        self.logPath = './mallHomePage_log/'
        self.logModule = "mallHomePage"        
        
        
        if Common().isLinux() is False:
            '''WIN'''
            self.homeUrl = '/mallhome/'
            self.searchUrl = '/mallsearch/'
            self.infoUrl = '/mallsearch/info/'
            
            self.sevIp = "127.0.0.1"
            self.sevPort = "8001"  
            
            self.redisRdIp = '120.26.117.54' # online1
            self.redisRdPort = 6390
            self.redisWrIp = '114.55.11.179' #online 4 主
            self.redisWrPort = 6393
            
            #mongodb
            self.mongodbIp = "114.55.11.179"#"121.43.200.103"
            self.mongodbPort =6391#27017

            #sql
            self.mysqlHost = "120.26.117.54"
            self.mysqlPort = 3306
            self.mysqlDatabase = "cateOptSys"
            self.mysqlUser = "55cateoptsys"
            self.mysqlPasswd = "55haitao"

            '''正规环境需要更新部署的内部接口'''
            self.getNaviUrl = "http://121.43.200.103:2700/mall/homepage/navi/get" # dev1 ?type=pre
            self.getBannerUrl = "http://121.43.200.103:2700/mall/homepage/banner/get?level=0" #dev1
            self.getFourAd = "http://121.43.200.103:2700/mall/homepage/fourAd/get"
            self.getSpecial = "http://121.43.200.103:2700/mall/homepage/special/get"
            self.getOfficalWebSale = "http://121.43.200.103:2700/mall/homepage/officalWebSale/get"
            self.getNewArrivals  = "http://121.43.200.103:2700/mall/homepage/newArrivals/get"
            self.getSubject = "http://121.43.200.103:2700/mall/homepage/subject/get"
            self.getFeature = "http://121.43.200.103:2700/mall/homepage/feature/get"
#             self.getSeller = "http://121.43.200.103:2700/mall/homepage/seller/get"
            self.getSeller = "http://120.26.117.54:8889/searchGET?query=*"
            self.getBrand = "http://121.43.200.103:2700/mall/homepage/brand/get"
            self.getBrandSearch = "http://121.43.200.103:2700/mall/homepage/brand/search?query="
            self.getOfficalWebSaleAll = "http://121.43.200.103:2700/mall/homepage/officalWebSale/get?type=1"
            
        else:
            '''LINUX'''
            self.homeUrl = '/mallhome/'
            self.searchUrl = '/mallsearch/'
            self.infoUrl = '/mallsearch/info/'
                    
            self.sevIp = "127.0.0.1"
            self.sevPort = "12910"
            
            self.redisRdIp = '10.51.35.123'
            self.redisRdPort = 6390
            self.redisWrIp = '10.25.1.67'
            self.redisWrPort = 6381
            
            #mongodb
            self.mongodbIp = "10.51.35.123" #online1
            self.mongodbPort = 6391

            #mysql配置
            self.mysqlHost = "10.51.35.123"
            self.mysqlPort = 3306
            self.mysqlDatabase = "cateOptSys"
            self.mysqlUser = "55cateoptsys"
            self.mysqlPasswd = "55haitao"
        
            '''正规环境需要更新部署的内部接口'''
            self.getNaviUrl = "http://127.0.0.1:2700/mall/homepage/navi/get" #dev1
            self.getBannerUrl = "http://127.0.0.1:2700/mall/homepage/banner/get?level=0" #dev1
            self.getFourAd = "http://127.0.0.1:2700/mall/homepage/fourAd/get"
            self.getSpecial = "http://127.0.0.1:2700/mall/homepage/special/get"
            self.getSpecialAll = "http://127.0.0.1:2700/mall/homepage/special/get?type=1"
            self.getOfficalWebSale = "http://127.0.0.1:2700/mall/homepage/officalWebSale/get"
            self.getNewArrivals = "http://127.0.0.1:2700/mall/homepage/newArrivals/get"
            self.getSubject = "http://127.0.0.1:2700/mall/homepage/subject/get"
            self.getFeature = "http://127.0.0.1:2700/mall/homepage/feature/get"
            self.getBrand = "http://127.0.0.1:2700/mall/homepage/brand/get"
            self.getBrandSearch = "http://127.0.0.1:2700/mall/homepage/brand/search?query="
#             self.getSeller = "http://127.0.0.1:2700/mall/homepage/seller/get"
            self.getSeller = "http://10.51.35.123:8889/searchGET?query=*"
            self.getOfficalWebSaleAll = "http://127.0.0.1:2700/mall/homepage/officalWebSale/get?type=1"
            

        


