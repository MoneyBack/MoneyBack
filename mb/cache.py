# -*- coding: utf-8 -*-
'''
Created on Jul 18, 2013

@author: Carl, Aaron
'''

'''
基于python-memcached的cache，可以存放不超过1M的数据，支持数据失效时间，是线程同步的
'''

from mcache import memcache
from mb.config import CACHE_SERVERS

class Cache():
    
    mc = None
    
    #初始化memcached环境
    def __init__(self):
        self.mc = memcache.Client(CACHE_SERVERS)
        
    def set(self, key, val, time=0):
        return self.mc.set(key, val, time=time)
    
    def get(self, key):
        return self.mc.get(key)
        
    def replace(self, key, val, time=0):
        return self.mc.replace(key, val, time=time)
    
    def delete(self, key, time=0):
        return self.mc.delete(key, time=time)
