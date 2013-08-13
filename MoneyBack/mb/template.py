# -*- coding: utf-8 -*-
'''
Created on Jul 11, 2013

@author: Carl
'''
import os
from mb.coordinator import _Pretty
from jinja2 import Environment,FileSystemLoader,TemplateNotFound
from mb.config import ERROR_NO_404, ERROR_NO_500

class Template(object):
    '''
    这里封装了Jinja2的模板引擎
    '''
    
    def render(self, templateName, **context):
        extensions = context.pop('extensions', [])
        globalVars = context.pop('globals', {})
        
        templatePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
        jinjaEnv = Environment(
                loader=FileSystemLoader(templatePath),
                extensions=extensions,
                )
        jinjaEnv.globals.update(globalVars)
        try:
            return jinjaEnv.get_template(templateName + ".html").render(context)
        except TemplateNotFound:
            _Pretty.handleError("Cannot find the template[" + templateName + "] in " + templatePath, ERROR_NO_404)
        except:
            errorInfo = os.sys.exc_info()
            _Pretty.handleError("Error '%s' happened on line %d\n" % (errorInfo[0], errorInfo[2].tb_lineno), ERROR_NO_500)