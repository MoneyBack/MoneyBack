# -*- coding: utf-8 -*-
'''
Created on Aug 13, 2013

@author: Carl, Aaron
'''

import sys
import threading
import Queue
import traceback
from mb.logger import MBLogger

_ASYNC = False

#与线程池相关的自定义异常
class NoResultsPending(Exception):
    """所有的请求都被处理了"""
    pass

class NoWorkersAvailable(Exception):
    """无可用工作线程"""
    pass


#异常发生时的处理函数
def handleThreadException(request, exc_info):
    """默认的错误发生时回调函数"""
    traceback.print_exception(*exc_info)
    MBLogger.error("Error occurred while handling the reqeust[" + str(request.taskID) + "]...", exc_info=True)

#构建一个请求
def makeTask(_callable, args, callback=None, errorCallback=handleThreadException):
    if isinstance(args, tuple):
        return WorkRequest(_callable, args[0], args[1], callback=callback,
            errorCallback=errorCallback)
    else:
        return WorkRequest(_callable, [args] if args else None, None, callback=callback,
            errorCallback=errorCallback)

#构建多个请求
def makeTasks(_callable, argsList, callback=None, errorCallback=handleThreadException):
    """构建一系列请求，相同的处理逻辑，不同的参数"""
    tasks = []
    for item in argsList:
        tasks.append(makeTask(_callable, item, None, callback=callback,
                    errorCallback=errorCallback))
    return tasks


#任务线程
class WorkerThread(threading.Thread):
    """从requestQueue中获取任务，完成后，把任务放入resultsQueue"""

    def __init__(self, tasksQueue, resultsQueue, pollTimeout=5, **kwds):
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(True)
        self.setName("[Pooled]-WorkerThread")
        self._tasksQueue = tasksQueue
        self._resultsQueue = resultsQueue
        self._pollTimeout = pollTimeout
        self._dismissed = threading.Event()
        self.start()

    def run(self):
        while True:
            if self._dismissed.isSet():
                # 请求退出
                break
            # 获取下个任务，阻塞timeout时间，如果没有取到一个Request，则从头开始
            try:
                request = self._tasksQueue.get(True, self._pollTimeout)
            except Queue.Empty:
                continue
            else:
                if self._dismissed.isSet():
                    # 放回获取的Request，并退出
                    self._tasksQueue.put(request)
                    break
                try:
                    # 有参数的方法
                    if request.args:
                        result = request.callable(*request.args, **request.kwds)
                    else:
                        # 无参数的方法
                        result = request.callable(**request.kwds)
                    # 异步回调
                    if _ASYNC:
                        self._resultsQueue.put((request, result))
                    else:
                        # 正常的处理完任务的回调
                        if request.callback:
                            request.callback(request, result)
                except:
                    request.exception = True
                    # 异步错误回调
                    if _ASYNC:
                        self._resultsQueue.put((request, sys.exc_info()))
                    else:
                        # 发生异常，错误回调
                        if request.exception and request.errorCallback:
                            request.errorCallback(request, sys.exc_info())

    def dismiss(self):
        """处理完当前任务后退出"""
        self._dismissed.set()

#一个任务请求
class WorkRequest:
    """任务请求，包含处理逻辑和参数以及回调函数"""

    def __init__(self, _callable, args=None, kwds=None, taskID=None,
            callback=None, errorCallback=handleThreadException):
        if taskID is None:
            self.taskID = id(self)
        else:
            try:
                self.taskID = hash(taskID)
            except TypeError:
                raise TypeError("taskID must be hashable.")
        self.exception = False
        self.callback = callback
        self.errorCallback = errorCallback
        self.callable = _callable
        self.args = args or []
        self.kwds = kwds or {}

    def __str__(self):
        return "<WorkRequest id=%s args=%r kwargs=%r exception=%s>" % \
            (self.taskID, self.args, self.kwds, self.exception)

class ThreadPool:
    """线程池核心逻辑"""

    def __init__(self, coreWorkers, pollTimeout=5):
        self._tasksQueue = Queue.Queue(0) #这里参数是Queue的最大值，0代表无限制，
        self._resultsQueue = Queue.Queue(0)
        self.workers = []
        self.dismissedWorkers = []
        self.workTasks = {}
        self.createWorkers(coreWorkers, pollTimeout)

    def createWorkers(self, coreWorkers, pollTimeout=5):
        """创建一些工作线程，并且设置一个获取的timeout，此timeout值也是检测该Request是否被dismissed的间隔时间"""
        for i in range(coreWorkers):
            self.workers.append(WorkerThread(self._tasksQueue,
                self._resultsQueue, pollTimeout=pollTimeout))

    def dismissWorkers(self, coreWorkers, doJoin=False):
        """告诉这些线程在完成当前任务后，停止"""
        dismissList = []
        for i in range(min(coreWorkers, len(self.workers))):
            worker = self.workers.pop()
            worker.dismiss()
            dismissList.append(worker)

        if doJoin:
            for worker in dismissList:
                worker.join()
        else:
            self.dismissedWorkers.extend(dismissList)

    def joinAllDismissedWorkers(self):
        for worker in self.dismissedWorkers:
            worker.join()
        self.dismissedWorkers = []

    def putTask(self, task, block=True, timeout=None):
        """增加一个任务到线程池"""
        self._tasksQueue.put(task, block, timeout)
        self.workTasks[task.taskID] = task

    def poll(self, block=False):
        while True:
            if not self.workTasks:
                raise NoResultsPending
            # 检测是否还有可用工作线程
            elif block and not self.workers:
                raise NoWorkersAvailable
            try:
                # 处理任务，返回结果
                request, result = self._resultsQueue.get(block=block)
                # 发生异常，错误回调
                if request.exception and request.errorCallback:
                    request.errorCallback(request, result)
                # 正常的处理完任务的回调
                if request.callback and not \
                       (request.exception and request.errorCallback):
                    request.callback(request, result)
                del self.workTasks[request.taskID]
            except Queue.Empty:
                break

    def wait(self):
        while True:
            try:
                self.poll(True)
            except NoResultsPending:
                break
