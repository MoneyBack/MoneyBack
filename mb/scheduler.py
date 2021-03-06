# -*- coding: utf-8 -*-
'''
Created on Aug 13, 2013

@author: Carl, Aaron
'''

import time
from mb.tasks import _AllianceTask
from mb.threadpool import *

allianceTask = makeTask(_AllianceTask.getCallable(), _AllianceTask.getArgs(), callback=_AllianceTask.getCallback())

#(Task, intervalTime, timestamp, taskName)
_NOW = int(time.time())
_SCHED_TASKS = [(allianceTask, 7 * 24 * 60 * 60, _NOW, "AllianceTask")]

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
