# -*- coding: utf-8 -*-
'''
Created on Aug 29, 2013

@author: Carl, Aaron
'''

from mb.db import MBDB

class TestDB:
    def GET(self):
        results = MBDB.select("student")
        for result in results:
            print( "id is %s, name is %s" % (result.id, result.name))
        return "hello world" 