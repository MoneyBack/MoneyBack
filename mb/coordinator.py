# -*- coding: utf-8 -*-
'''
Created on Jul 18, 2013

@author: Carl, Aaron
'''

import os
import web
import mb
from web.webapi import HTTPError
from mb.logger import MBLogger
from mb.config import ERROR_NO_404_STR, ERROR_NO_500_STR, START_LOCAL_CACHE_SERVER_CMD
from mb.actions import homeAction
from mb.scheduler import Scheduler
from mb.db import MBDB

#模板
_Template = None

class Context():
    def init(self):
        os.system(START_LOCAL_CACHE_SERVER_CMD)
        global _Template
        _Template  = mb.template.Template()
        _MBDB = MBDB
        _scheduler = Scheduler()

class Home:
    def GET(self):
        homeData, jsonStr = homeAction.getData()
        return _Template.render("home", data=jsonStr or {}, **homeData)

class Redirect:
    def GET(self, path):
        web.seeother('/' + path)

class AboutUs:
    def GET(self):
        return _Template.render("about")
    
class OpenSite:
    def POST(self):
        siteId = web.input()['siteId']
        if siteId:
            homeAction.openSite(siteId)

class Pretty(object):
    def handleError(self, message, errno):
        MBLogger.error(message)
        self.handle(errno)

    def handle(self, errno):
        web.seeother('/error/' + str(errno))

    def handle404(self):
        return _Template.render("page_404")

    def handle500(self):
        return _Template.render("page_500")

#以好看的样式处理错误
_Pretty = Pretty()

class Error:
    '''
    错误处理
    '''
    def __init__(self):
        self._mapping = {
            ERROR_NO_404_STR : lambda : _Pretty.handle404(),
            ERROR_NO_500_STR : lambda : _Pretty.handle500()
        }
    def GET(self, errno):
        return self._mapping[str(errno)]()

class _NotFound(HTTPError):
    """`404 Not Found` error."""
    def __init__(self):
        status = '404 Not Found'
        headers = {'Content-Type': 'text/html'}
        HTTPError.__init__(self, status, headers, _Pretty.handle404())

class _InternalError(HTTPError):
    """500 Internal Server Error`."""
    def __init__(self):
        status = '500 Internal Server Error'
        headers = {'Content-Type': 'text/html'}
        HTTPError.__init__(self, status, headers, _Pretty.handle500())

def NotFound(message=None):
    """Returns HTTPError with '404 Not Found' error from the active application.
    """
    return _NotFound()

def InternalError(message=None):
    """Returns HTTPError with '500 internal error' error from the active application.
    """
    return _InternalError()
