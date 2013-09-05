# -*- coding: utf-8 -*-
'''
Created on Jul 18, 2013

@author: Carl, Aaron
'''

from logger import MBLogger

class CacheInvalidError(Exception):
    '''Cache数据过期'''
    pass

class ServerError(Exception):
    '''
    各种Server错误
    '''
    _errno = None
    _message = None
    
    def __init__(self, message, errno):
        Exception.__init__(self)
        self._message = message
        self._errno = errno
        
    def details(self):
        MBLogger.error("Error occurred, message(" + self._message + "), code(" + self._errno + ").")