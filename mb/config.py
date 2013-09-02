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

STATUS_FOLDER_NAME = ".status"
STATUS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), '%s%s' % (STATUS_FOLDER_NAME, os.path.sep))
'''如果状态文件夹不存在，则创建该文件夹'''
if not os.path.exists(STATUS_FOLDER):
    os.makedirs(STATUS_FOLDER)

#################联盟相关配置 Start###################
APP_KEY = "137568413663310785"
APP_SECRET = "5d3c9a369a9554f153f9f3fb0bfb4365"

WEBSITE_TYPE_BUSINESS = "1"
WEBSITE_TYPE_COMMODITY = "2"
WEBSITE_CATEGORY_REQUEST_FIELDS = "web_catid,web_cname,amount,web_type,modified_time,total"
WEBSITE_LIST_REQUEST_FIELDS = "web_id,web_name,web_catid,logo_url,web_o_url,commission,total"
#################联盟相关配置 End  ###################

#################Session相关配置 Start###################
SESSION_COOKIE_NAME = 'mb_session_id'
SESSION_TIMEOUT = 30 * 60 #半个小时
#################Session相关配置 End  ###################

#################Cache相关配置 Start###################
CACHE_HOST = '127.0.0.1'
CACHE_PORT = 12000
CACHE_SERVERS=['127.0.0.1:%d' % CACHE_PORT]
CACHE_MEM_SIZE = 100
CACHE_PID_FILE = '/tmp/memcached.pid'
START_LOCAL_CACHE_SERVER_CMD = 'memcached -d -m %d -p %d -P %s' % (CACHE_MEM_SIZE, CACHE_PORT, CACHE_PID_FILE)
STOP_LOCAL_CACHE_SERVER_CMD = 'kill `cat %s`' % CACHE_PID_FILE
CACHE_PREFIX_ALLIANCE = 'alliance_'
CACHE_PREFIX_CATRGORY = 'alliance_cats'
CACHE_PREFIX_SUB_CATEGORY = 'alliance_sub_cat_'
#################Cache相关配置 End  ###################

############database configure information############
DB_USER = 'root'
DB_PASSWD = 'rootpwd'
DB_INITED_STATUS = 'mb_db_inited'
INIT_DEV_ENV = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db%sinit_env.sql' % os.path.sep)
INIT_TABLES = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db%sinit_tables.sql' % os.path.sep)
DB_INITED = os.path.join(STATUS_FOLDER, DB_INITED_STATUS)

DB_TABLE_ELECTRIC_PURCHASER = 'electric_purchaser'
DB_TABLE_PERSONAL_PAGE = 'personal_page'
DB_TABLE_USER_INFO = 'user_info'
DB_TABLE_USER_BANK_ACCOUNT = 'user_bank_account'

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
