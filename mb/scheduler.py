# -*- coding: utf-8 -*-
'''
Created on Aug 13, 2013

@author: Carl, Aaron
'''

import time
import json
from mb.config import WEBSITE_TYPE_BUSINESS, WEBSITE_CATEGORY_REQUEST_FIELDS, WEBSITE_LIST_REQUEST_FIELDS, APP_KEY, APP_SECRET
from mb.alliance import YiqifaAPI, WebsiteCategoryReqeust, WebsiteListRequest
from mb.threadpool import *

#################Task相关配置 Start###################
'''获取联盟信息Task'''

class AllianceError(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return repr(self.message)

'''处理联盟信息的回调函数'''
def handleAllianceInfo(request, result):
    print result
    
'''
{"web_catid":"2","web_cname":"服装服饰","amount":"22","web_type":"2","modified_time":"2013-02-02 11:09:00"},
{"web_catid":"4","web_cname":"美容化妆","amount":"15","web_type":"2","modified_time":"2013-02-02 11:09:00"},
{"web_catid":"5","web_cname":"家居家饰","amount":"11","web_type":"2","modified_time":"2013-02-02 11:09:00"},
{"web_catid":"24","web_cname":"网络服务/其他","amount":"1","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"25","web_cname":"名品特卖","amount":"2","web_type":"2","modified_time":"2013-02-02 11:09:00"},
{"web_catid":"7","web_cname":"母婴/儿童用品","amount":"5","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"9","web_cname":"鲜花礼品","amount":"1","web_type":"2","modified_time":"2013-02-02 11:09:00"},
{"web_catid":"13","web_cname":"成人保健","amount":"5","web_type":"2","modified_time":"2013-02-02 11:09:00"},
{"web_catid":"15","web_cname":"运动户外","amount":"3","web_type":"2","modified_time":"2013-02-02 11:09:00"},
{"web_catid":"18","web_cname":"电视购物","amount":"6","web_type":"2","modified_time":"2013-02-02 11:09:00"},
{"web_catid":"10","web_cname":"珠宝首饰","amount":"7","web_type":"2","modified_time":"2013-02-02 11:09:00"},
{"web_catid":"26","web_cname":"奢侈品","amount":"5","web_type":"2","modified_time":"2013-02-02 11:09:00"},
{"web_catid":"11","web_cname":"食品/茶叶/酒水","amount":"19","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"12","web_cname":"医药健康","amount":"16","web_type":"2","modified_time":"2013-02-02 11:09:00"},
{"web_catid":"16","web_cname":"箱包/眼镜/鞋类","amount":"20","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"1","web_cname":"综合商城","amount":"25","web_type":"2","modified_time":"2013-02-02 11:09:00"},
{"web_catid":"17","web_cname":"团购","amount":"3","web_type":"2","modified_time":"2013-02-02 11:09:00"},
{"web_catid":"3","web_cname":"手机/数码/家电","amount":"19","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"6","web_cname":"女性/内衣","amount":"2","web_type":"2","modified_time":"2013-02-02 11:09:00"},
{"web_catid":"8","web_cname":"图书音像","amount":"9","web_type":"2","modified_time":"2013-02-02 11:09:00"}
---------------------------------
{"request":"http://openapi.yiqifa.com/api2/open.website.category.get.json","response":{"web_cats":{"web_cat":[{"web_catid":"2","web_cname":"服装服饰","amount":"22","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"4","web_cname":"美容化妆","amount":"15","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"5","web_cname":"家居家饰","amount":"11","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"24","web_cname":"网络服务/其他","amount":"1","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"25","web_cname":"名品特卖","amount":"2","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"7","web_cname":"母婴/儿童用品","amount":"5","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"9","web_cname":"鲜花礼品","amount":"1","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"13","web_cname":"成人保健","amount":"5","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"15","web_cname":"运动户外","amount":"3","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"18","web_cname":"电视购物","amount":"6","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"10","web_cname":"珠宝首饰","amount":"7","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"26","web_cname":"奢侈品","amount":"5","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"11","web_cname":"食品/茶叶/酒水","amount":"19","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"12","web_cname":"医药健康","amount":"16","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"16","web_cname":"箱包/眼镜/鞋类","amount":"20","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"1","web_cname":"综合商城","amount":"25","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"17","web_cname":"团购","amount":"3","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"3","web_cname":"手机/数码/家电","amount":"19","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"6","web_cname":"女性/内衣","amount":"2","web_type":"2","modified_time":"2013-02-02 11:09:00"},{"web_catid":"8","web_cname":"图书音像","amount":"9","web_type":"2","modified_time":"2013-02-02 11:09:00"}]},"total":"20"}}
---------------------------------
{"errors":{"error":[{"request":"http://openapi.yiqifa.com/api2/open.website.list.get.json","error_code":"C0000","msg":"catid:missing required parameters;"},{"request":"http://openapi.yiqifa.com/api2/open.website.list.get.json","error_code":"C0004","msg":"catId:request param is not supply ;"}]}}
'''
    
def getWebsiteList():
    webCats = getCategory()
    wcr = WebsiteListRequest(WEBSITE_LIST_REQUEST_FIELDS, webCats, WEBSITE_TYPE_BUSINESS)
    apiObj = YiqifaAPI(APP_KEY, APP_SECRET)
    webCatsJsonStr = apiObj.call(wcr)
    MBLogger.info("Alliance Website lists Information: %s" % webCatsJsonStr)
    webCatsJson = json.loads(webCatsJsonStr)
    if webCatsJson.has_key('errors'):
        errors = []
        for errorInfo in webCatsJson['errors']['error']:
            errors.append("ErrorCode[%s] - Message[%s]" % (errorInfo['error_code'], errorInfo['msg']))
        raise AllianceError(",".join(errors))
    return webCatsJsonStr
    
def getCategory():
    wcr = WebsiteCategoryReqeust(WEBSITE_CATEGORY_REQUEST_FIELDS, WEBSITE_TYPE_BUSINESS)
    apiObj = YiqifaAPI(APP_KEY, APP_SECRET)
    categoryJsonStr = apiObj.call(wcr)
    MBLogger.info("Alliance Category Information: %s" % categoryJsonStr)
    categoryJson = json.loads(categoryJsonStr)
    if categoryJson.has_key('errors'):
        errors = []
        for errorInfo in categoryJson['errors']['error']:
            errors.append("ErrorCode[%s] - Message[%s]" % (errorInfo['error_code'], errorInfo['msg']))
        raise AllianceError(",".join(errors))
    webCats = []
    for webCategoryInfo in categoryJson['response']['web_cats']['web_cat']:
        webCats.append(webCategoryInfo['web_catid'])
    return ",".join(webCats)

allianceTask = makeTask(getWebsiteList, None, callback=handleAllianceInfo)

#(Task, intervalTime, timestamp, taskName)
_NOW = int(time.time())
_SCHED_TASKS = [(allianceTask, 1 * 24 * 60 * 60, _NOW, "AllianceTask")]
#################Task相关配置 End  ###################

class Scheduler(threading.Thread):
    
    #内置
    _pool = None
    _dismissed = threading.Event()
    _waiter = threading.Event()
    _taskList = None
    
    def __init__(self, **kwds):
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(True)
        self.setName("SchedulerThread")
        self._pool = ThreadPool(5)
        self._taskList = _SCHED_TASKS
        self.start()
    
    #关闭调度线程
    def dismiss(self):
        self._dismissed.set()
        self._waiter.set()
    
    #按照timestamp来排序  
    def sort(self, taskList):
        taskList.sort(key=lambda task : task[2], reverse=True)
    
    def run(self):
        self.sort(self._taskList)
        while True:
            if self._dismissed.is_set():
                break
            task = self._taskList.pop()
            self.waitAndFire(task)
    
    #等待触发执行任务，并重新计算下次触发时间        
    def waitAndFire(self, task):
        # 等待时间 = 上次时间戳 - 当前时间
        waitTime = task[2] - int(time.time())
        if waitTime > 0:
            self._waiter.wait(waitTime)
        if not self._dismissed.is_set():
            self._taskList.append((task[0], task[1], int(time.time()) + task[1], task[3]))
            self.fire(task[0], task[3])
            self.sort(self._taskList)
    
    #把任务放入任务池，执行任务
    def fire(self, task, taskName):
        MBLogger.info("Fire Task [%s] ... " % taskName)
        self._pool.putTask(task)
