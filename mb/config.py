# -*- coding: utf-8 -*-
'''
Created on Jul 11, 2013

@author: Carl
'''

import string

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
