# -*- coding: utf-8 -*-
'''
Created on Jul 18, 2013

@author: Carl, Aaron
'''

import json

# 各种工具方法
class Util():
    
    def toJson(self, jsonStr):
        return json.loads(jsonStr)
    
    def toJsonStr(self, obj):
        return json.dumps(obj)
    
MBUtils = Util()