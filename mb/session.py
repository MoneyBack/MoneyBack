# -*- coding: utf-8 -*-
'''
Created on Sep 1, 2013

@author: Carl, Aaron
'''

import web
from mb.config import SESSION_COOKIE_NAME, SESSION_TIMEOUT, CACHE_SERVERS
from mcache import memcache

web.config.session_parameters["cookie_name"] = SESSION_COOKIE_NAME
web.config.session_parameters["timeout"] = SESSION_TIMEOUT

class MemCacheStore(web.session.Store):
    
    mc = None
    
    def __init__(self):
        self.mc = memcache.Client(CACHE_SERVERS, debug=0)

    def __contains__(self, key):
        return self.mc.get(key) != None

    def __getitem__(self, key):
        return self.mc.get(key)

    def __setitem__(self, key, value):
        self.mc.set(key, value, time = web.config.session_parameters["timeout"])

    def __delitem__(self, key):
        self.mc.delete(key)

    def cleanup(self, timeout):
        # Not needed as we assigned the timeout to memcache
        pass
