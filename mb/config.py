# -*- coding: utf-8 -*-
'''
Created on Jul 11, 2013

@author: Carl, Aaron
'''

import string
from mb.alliance import YiqifaAPI, WebsiteCategoryReqeust

urls = (
    '/', 'Home',
    '/(.*)/', 'Redirect',
    '/error/(\d+)', 'Error',
    '/about_us', 'AboutUs'
)

ERROR_NO_404_STR = "404"
ERROR_NO_500_STR = "500"

ERROR_NO_404 = string.atoi(ERROR_NO_404_STR)
ERROR_NO_500 = string.atoi(ERROR_NO_500_STR)

APP_KEY = "137568413663310785"
APP_SECRET = "5d3c9a369a9554f153f9f3fb0bfb4365"

wcr = WebsiteCategoryReqeust("web_catid,web_cname,amount,web_type,modified_time,total", "1")
apiObj = YiqifaAPI(APP_KEY, APP_SECRET)
result = apiObj.call(wcr)
