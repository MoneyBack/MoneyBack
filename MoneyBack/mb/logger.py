# -*- coding: utf-8 -*-
'''
Created on Jul 11, 2013

@author: Carl
'''

import os
import logging
from logging.handlers import RotatingFileHandler

LOG_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs' + os.path.sep)
'''如果日志文件夹不存在，则创建该文件夹'''
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

MBLogger = logging.getLogger('MBLogger')
logging.basicConfig(level=logging.DEBUG, datefmt='%d %b %Y %H:%M:%S', filemode='w')
rthandler = RotatingFileHandler(LOG_FOLDER + 'MBApp.log', maxBytes=10*1024*1024, backupCount=5)
rtFormatter = logging.Formatter('%(asctime)s %(filename)-12s[line:%(lineno)d] %(levelname)-8s %(message)s')
rthandler.setFormatter(rtFormatter)
rthandler.setLevel(logging.DEBUG)

MBLogger.addHandler(rthandler)
MBLogger.debug('logging init ...')

