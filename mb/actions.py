# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2013

@author: Carl, Aaron
'''
from mb.config import DB_TABLE_ELECTRIC_PURCHASER
from mb.db import MBDB
from mb.cache import MBCache
from mb.config import CACHE_PREFIX_ALLIANCE, CACHE_CATRGORYS, CACHE_PREFIX_SUB_CATEGORY
from mb.exceptions import CacheInvalidError
import threading
import web

class HomeAction():
    
    _UPDATE_CACHE = 'UpdatingHomeDataCache'
    _waiter = threading.Event()
    
    def getSession(self):
        # 读取Cookie信息，检测Session是否需要重新生成
        mbSession = web.ctx.session
        # 如果已经登录
        if mbSession.loginLevel > 0:
            pass
        else:
            # 未登录，检查Cookie信息，（如果有登录信息则重新生成Session，否则为匿名用户）
            mbCookie = web.cookies()
            mbCookie.get('')
        web.ctx.session.myFavSites=['test']
        return web.ctx.session
    
    #先从缓存取相关信息，如果没有则从数据库取信息并放入缓存
    def getData(self):
        homeData = None
        session = self.getSession()
        try:
            homeData = self.getHomeDataFromCache()
        except CacheInvalidError:
            homeData = self.getHomeData()
        homeData['userInfo'] = session.userInfo
        # 已登录用户
        if session.loginLevel > 0:
            homeData['myFavSites'] = session.myFavSites
            homeData['loggedIn'] = True
        # Guest用户
        else:
            homeData['myFavSites'] = self.getDefaultFavSites()
            homeData['loggedIn'] = False
        return homeData
        
    def getDefaultFavSites(self):
        # 获取默认的自定义页信息
        return []
    
    def getHomeDataFromCache(self):
        while MBCache.get(self._UPDATE_CACHE):
            self._waiter.wait(1)
        homeData = {'sites':{}, 'categoryMap':{}, 'categorys':[], 'myFavSites':[]}
        allCategorys = MBCache.get(CACHE_CATRGORYS)
        if not allCategorys:
            raise CacheInvalidError
        homeData['categorys'] = allCategorys
        for category in allCategorys:
            catSites = MBCache.get('%s%s' % (CACHE_PREFIX_SUB_CATEGORY, category))
            if not catSites:
                raise CacheInvalidError
            homeData['categoryMap'][category] = catSites
            for site in catSites:
                siteInfo = MBCache.get('%s%s' % (CACHE_PREFIX_ALLIANCE, site))
                if not siteInfo:
                    raise CacheInvalidError
                homeData['sites'][site] = siteInfo
        return homeData
    
    def getHomeData(self):
        MBCache.set(self._UPDATE_CACHE, True)
        homeData = {'sites':{}, 'categoryMap':{}, 'categorys':[], 'myFavSites':[]}
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
        MBCache.delete(self._UPDATE_CACHE)
        return homeData
        

homeAction = HomeAction()
