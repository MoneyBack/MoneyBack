# -*- coding: utf-8 -*-
'''
Created on Aug 29, 2013

@author: Carl, Aaron
'''

import web
from mbtest import *

urls = (
    '/', 'index',
    '/test_db', 'TestDB'
)

class index:
    def GET(self):
        return "Hello, world!"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()