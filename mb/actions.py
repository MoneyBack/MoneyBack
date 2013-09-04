# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2013

@author: Carl, Aaron
'''
from mb.config import DB_TABLE_ELECTRIC_PURCHASER
from mb.db import MBDB
from mb.cache import MBCache
from mb.config import CACHE_PREFIX_ALLIANCE, CACHE_CATRGORYS, CACHE_PREFIX_SUB_CATEGORY

class HomeAction():
    
    def getHomeData(self):
        homeData = {'sites':{}, 'categoryMap':{}, 'categorys':[]}
        #先从缓存取相关信息，如果没有则从数据库取信息并放入缓存
        allSiteInfos =  MBDB.select(DB_TABLE_ELECTRIC_PURCHASER)
        allCatSet = set()
        catSiteMap = dict()
        for siteInfo in allSiteInfos:
            merchantId = str(siteInfo.merchant_id)
            merchantCatId = str(siteInfo.merchant_cat_id)
            allCatSet.add(merchantCatId)
            catSites = catSiteMap.get(merchantCatId)
            if catSites:
                catSites.append(merchantId)
            else:
                catSiteMap[merchantCatId] = [merchantId]
            MBCache.set('%s%s' % (CACHE_PREFIX_ALLIANCE, merchantId), siteInfo)
            homeData['sites'][merchantId] = siteInfo
        MBCache.set(CACHE_CATRGORYS, list(allCatSet))
        homeData['categorys'] = list(allCatSet)
        for (k, v) in catSiteMap.items():
            MBCache.set('%s%s' % (CACHE_PREFIX_SUB_CATEGORY, k), v)
            homeData['categoryMap'][k] = v
        return homeData
        

homeAction = HomeAction()
