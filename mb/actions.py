# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2013

@author: Carl, Aaron
'''
from mb.config import DB_TABLE_ELECTRIC_PURCHASER, DEFAULT_FAV_SITES
from mb.db import MBDB
from mb.cache import MBCache
from mb.config import CACHE_PREFIX_ALLIANCE, CACHE_CATRGORYS, CACHE_PREFIX_SUB_CATEGORY
from mb.exceptions import CacheInvalidError
import threading
import web
from mb.logger import MBLogger
from mb.utils import MBUtils

class HomeAction():
    
    _UPDATE_CACHE = 'UpdatingHomeDataCache'
    _waiter = threading.Event()
    
    def getSession(self, urlIdMap):
        # 读取Cookie信息，检测Session是否需要重新生成
        mbSession = web.ctx.session
        # 未登录，检查Cookie信息，（如果有登录信息则重新生成Session，否则为匿名用户）
        if not mbSession.loggedIn:
            mbCookie = web.cookies()
            userId = mbCookie.get('userId')
            userName = mbCookie.get('userName')
            # 检测到Cookie信息
            if userId and userName:
                mbSession.loggedIn = True
                mbSession.userInfo.userId = userId
                mbSession.userInfo.userName = userName
            myFavSites = mbCookie.get('myFavSites')
            if myFavSites:
                mbSession.myFavSites = myFavSites.split(',')
            else:
                mbSession.myFavSites = self.getDefaultFavSites(urlIdMap)
                web.setcookie('myFavSites', ','.join(mbSession.myFavSites), 24 * 60 * 60)
        return mbSession
    
    def getDefaultFavSites(self, urlIdMap):
        # 获取默认的自定义页信息
        defaultFavSites = []
        for siteUrl in DEFAULT_FAV_SITES:
            defaultFavSites.append(urlIdMap[siteUrl])
        return defaultFavSites
    
    #先从缓存取相关信息，如果没有则从数据库取信息并放入缓存
    def getData(self):
        homeData = None
        try:
            homeData = self.getHomeDataFromCache()
        except CacheInvalidError:
            homeData = self.getHomeData()
        if homeData:
            session = self.getSession(homeData['urlSiteIdMap'])
            homeData['userInfo'] = session.userInfo
            homeData['myFavSites'] = session.myFavSites
            homeData['loggedIn'] = session.loggedIn
        else:
            MBLogger.error('Failed to fetch the home information ... ')
        return (homeData, MBUtils.toJsonStr(homeData) if homeData else None)
        
    def getHomeDataFromCache(self):
        while MBCache.get(self._UPDATE_CACHE):
            self._waiter.wait(1)
        homeData = {'sites':{}, 'categoryMap':{}, 'urlSiteIdMap':{}, 'categorys':[], 'myFavSites':[]}
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
                homeData['urlSiteIdMap'][siteInfo['url']] = site
        return homeData
    
    def getHomeData(self):
        MBCache.set(self._UPDATE_CACHE, True)
        homeData = None
        try:
            homeData = {'sites':{}, 'categoryMap':{}, 'urlSiteIdMap':{}, 'categorys':[], 'myFavSites':[]}
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
                MBCache.set('%s%s' % (CACHE_PREFIX_ALLIANCE, merchantId), dict(siteInfo))
                homeData['sites'][merchantId] = dict(siteInfo)
                homeData['urlSiteIdMap'][siteInfo['url']] = merchantId
            MBCache.set(CACHE_CATRGORYS, list(allCatSet))
            homeData['categorys'] = list(allCatSet)
            for (k, v) in catSiteMap.items():
                MBCache.set('%s%s' % (CACHE_PREFIX_SUB_CATEGORY, k), v)
                homeData['categoryMap'][k] = v
        finally:
            MBCache.delete(self._UPDATE_CACHE)
        return homeData
    
    def openSite(self, siteId):
        MBDB.query("update %s set click_rate=click_rate+1 where merchant_id=$merchant_id" % DB_TABLE_ELECTRIC_PURCHASER,
            sql_vars={'merchant_id':siteId})
        

homeAction = HomeAction()
