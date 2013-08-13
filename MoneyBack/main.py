# -*- coding: utf-8 -*-
'''
Created on Jul 8, 2013

@author: Carl
'''
#############Avoid Apache import error#############
import os
import sys

curdir = os.path.dirname(__file__)
sys.path.insert(0, curdir)
###################################################

from mb.caretaker import Caretaker

_Caretaker = Caretaker()

####Apache WSGI Module need a application field####
application = _Caretaker.getWebApp()
###################################################

if __name__ == "__main__":
	_Caretaker.start()
