# -*- coding: utf-8 -*-
'''
Created on Aug 29, 2013

@author: Carl, Aaron
'''
import os
import sys

curdir = os.path.dirname(__file__)
sys.path.insert(0, curdir)

import web
from mbtest.testDb import TestDB

urls = (
    '/', 'index',
    '/test_db', 'TestDB'
)

app = web.application(urls, globals())
application = app.wsgifunc()

class index:
    def GET(self):
        return "Hello, world!"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
