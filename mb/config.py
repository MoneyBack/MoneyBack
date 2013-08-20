# -*- coding: utf-8 -*-
'''
Created on Jul 11, 2013

@author: Carl, Aaron
'''

import os
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

#################联盟相关配置 Start###################
APP_KEY = "137568413663310785"
APP_SECRET = "5d3c9a369a9554f153f9f3fb0bfb4365"

WEBSITE_TYPE = "1"
WEBSITE_TYPE = "2"
WEBSITE_CATEGORY_REQUEST_FIELDS = "web_catid,web_cname,amount,web_type,modified_time,total"
WEBSITE_LIST_REQUEST_FIELDS = "web_id,web_name,web_catid,logo_url,web_o_url,commission,total"
#################联盟相关配置 End  ###################

############database configure information############
DB_USER = 'root'
DB_PASSWD = 'rootpwd'
INIT_DEV_ENV = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db%sinitDevEnv.sql' % os.sep)
INIT_TABLES = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db%sinit_tables.sql' % os.sep)
#Master read/write database
DB_MASTER_TYPE = 'mysql'
DB_MASTER_HOST = 'localhost'
DB_MASTER_DBNAME = 'moneyBack'
DB_MASTER_USER = 'mbuser'
DB_MASTER_PASSWD = 'mbfighter'
#Slave read database - server behind HA proxy of mysql
DB_SLAVE_TYPE = 'mysql'
DB_SLAVE_HOST = 'localhost'
DB_SLAVE_DBNAME = 'moneyBack'
DB_SLAVE_USER = 'mbuser'
DB_SLAVE_PASSWD = 'mbfighter'
############database configure information############
