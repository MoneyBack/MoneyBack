# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2013

@author: Carl, Aaron
'''
from mb.config import DB_TABLE_ELECTRIC_PURCHASER
from mb.db import MBDB

class HomeAction():
    
    def getHomeData(self):
        MBDB.select(DB_TABLE_ELECTRIC_PURCHASER, where="", sql_vars="")
        pass

homeAction = HomeAction()