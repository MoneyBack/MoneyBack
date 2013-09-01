# -*- coding: utf-8 -*-
'''
Created on Jul 18, 2013

@author: Carl, Aaron
'''

from mb.config import urls
from mb.coordinator import *
from mb.session import MemCacheStore

class Caretaker(object):
    '''
    整个系统的掌管者
    '''
    
    def __init__(self):
        Context().init()
        
    def start(self):
        self.startWebServer()
            
    def startWebServer(self):
        MBLogger.info('Starting Server ...')
        web.webapi.notfound = NotFound
        web.webapi.internalerror = InternalError
        web.config.debug = False
        app = web.application(urls, globals())
        self.initSession(app)
        app.add_processor(web.loadhook(self.sessionHook))
        app.run()
        
    def getWebApp(self):
        MBLogger.info('Initializing Web Application ...')
        web.webapi.notfound = NotFound
        web.webapi.internalerror = InternalError
        web.config.debug = False
        app = web.application(urls, globals())
        self.initSession(app)
        app.add_processor(web.loadhook(self.sessionHook))
        return app.wsgifunc()
    
    def initSession(self, app):
        self.session = web.session.Session(app, MemCacheStore(), initializer={'username':'Guest'})
        
    def sessionHook(self):
        web.ctx.session = self.session
