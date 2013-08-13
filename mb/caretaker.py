# -*- coding: utf-8 -*-
'''
Created on Jul 18, 2013

@author: Carl, Aaron
'''

from mb.config import urls
from mb.coordinator import *

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
        app.run()
        
    def getWebApp(self):
        web.webapi.notfound = NotFound
        web.webapi.internalerror = InternalError
        web.config.debug = False
        return web.application(urls, globals()).wsgifunc()
