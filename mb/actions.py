# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2013

@author: Carl, Aaron
'''
from mb.config import DB_TABLE_ELECTRIC_PURCHASER
from mb.db import MBDB
from mb.cache import MBCache

class HomeAction():
    
    def getHomeData(self):
        homeData = {}
        #先从缓存取相关信息，如果没有则从数据库取信息并放入缓存
        allSiteInfos =  MBDB.select(DB_TABLE_ELECTRIC_PURCHASER)
        for siteInfo in allSiteInfos:
            pass
        return homeData
        

homeAction = HomeAction()

