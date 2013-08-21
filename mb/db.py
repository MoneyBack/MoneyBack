# -*- coding: utf-8 -*-
'''
Created on Jul 11, 2013

@author: Carl, Aaron
'''

import subprocess
import web, config
from logger import MBLogger

class MBDB():
    def __init__(self):
        self.execSQLBatch('mysql -u%s -p%s' % (config.DB_USER, config.DB_PASSWD), 'source ' + config.INIT_DEV_ENV, "Init Environment", "Error occurred while initializing development environment")
        self.execSQLBatch('mysql -u%s -p%s' % (config.DB_USER, config.DB_PASSWD), 'source ' + config.INIT_TABLES, "Init Tables", "Error occurred while initializing development environment")
        
    
    def execSQLBatch(self, cmd, subCmd, debugTag, errorTag):
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
            output = process.communicate(subCmd)
            MBLogger.debug("%s ... %s" % (debugTag, output[0]))
            if (output[1]):
                MBLogger.error("%s ... %s" % (errorTag, output[1]))
        except:
            MBLogger.error("Error occurred while executing the sql batch ...", exc_info=True)
        


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
