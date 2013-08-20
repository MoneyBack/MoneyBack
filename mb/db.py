# -*- coding: utf-8 -*-
'''
Created on Jul 11, 2013

@author: Carl, Aaron
'''

import subprocess
import web, config

class MBDB():
    def __init__(self):
        process = subprocess.Popen('mysql -u%s -p%s' % (config.DB_USER, config.DB_PASSWD), stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        output = process.communicate('source ' + config.INIT_DEV_ENV)
        output = process.communicate('source ' + config.INIT_TABLES)


master = web.database(
            dbn = config.DB_MASTER_TYPE,
            host = config.DB_MASTER_HOST,
            db = config.DB_MASTER_DBNAME,
            user = config.DB_MASTER_USER,
            pw = config.DB_MASTER_PASSWD
        )

slave = web.database(
            dbn = config.DB_SLAVE_TYPE,
            host = config.DB_SLAVE_HOST,
            db = config.DB_SLAVE_DBNAME,
            user = config.DB_SLAVE_USER,
            pw = config.DB_SLAVE_PASSWD
        )
