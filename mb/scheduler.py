# -*- coding: utf-8 -*-
'''
Created on Aug 13, 2013

@author: Carl, Aaron
'''
from mb.config import WEBSITE_TYPE, WEBSITE_CATEGORY_REQUEST_FIELDS, APP_KEY, APP_SECRET
from mb.alliance import YiqifaAPI, WebsiteCategoryReqeust
from mb.threadpool import *

#################Task相关配置 Start###################
'''获取联盟信息Task'''
wcr = WebsiteCategoryReqeust(WEBSITE_CATEGORY_REQUEST_FIELDS, WEBSITE_TYPE)
apiObj = YiqifaAPI(APP_KEY, APP_SECRET)

'''处理联盟信息的回调函数'''
def handleAllianceInfo(result):
    print result

allianceTask = makeTask(apiObj.call, wcr, callback=handleAllianceInfo)

#(Task, intervalTime, waitTime)
_SCHED_TASKS = [(allianceTask, 1 * 24 * 60 * 60, 0)]
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
    
    #按照waitTime来排序  
    def sort(self, taskList):
        sorted(taskList, key=lambda task : task[2])
    
    def run(self):
        self.sort(self._taskList)
        while True:
            if self._dismissed.is_set():
                break
            task = self._taskList.pop()
            self.waitAndFire(task)
    
    #等待触发执行任务，并重新计算下次触发时间        
    def waitAndFire(self, task):
        if task[2] > 0:
            self._waiter.wait(task[2])
        if not self._dismissed.is_set():
            self._taskList.append((task[0], task[1], task[1]))
            self.fire(task[0])
            self.sort(self._taskList)
    
    #把任务放入任务池，执行任务
    def fire(self, task):
        self._pool.putTask(task)
