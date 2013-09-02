# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2013

@author: Carl, Aaron
'''
from mb.config import DB_TABLE_ELECTRIC_PURCHASER
from mb.db import MBDB

class HomeAction():
    
    def getHomeData(self):
        homeData = {}
        allSiteInfos =  MBDB.select(DB_TABLE_ELECTRIC_PURCHASER)
        for siteInfo in allSiteInfos:
            pass
        return homeData
        

homeAction = HomeAction()

