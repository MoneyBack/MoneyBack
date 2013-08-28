# -*- coding: utf-8 -*-
'''
Created on Jul 11, 2013

@author: Carl, Aaron
'''

import subprocess
import web, config
from logger import MBLogger

'''
创建/连接数据库对象：

db = web.database(dbn='mysql', user='user', pw='pass', db='dbname')

查询：
users = db.query('select * from user where id>$id', vars={'id':100})

for user in users: print user.id, user.name

查询参数用$var_name表示，查询时用vars dict中的值替换

查询得到的是迭代对象，直接循环

至于每个对象的具体属性，和字段名一一对应。没有任何预定义的class，没有映射和配置，一切都是约定，你需要的是自己管理好数据库字段的命名。

插入：
db.insert('user', name='Michael', age=29, passwd='passwd', email='abc@xyz.com')

插入利用了python的**kw提供字段值，非常方便

修改：
db.update('user', where='id=$id', vars={'id':100}, name='Michael', age=29)

update也充分利用了python的**kw参数，只有传入的**kw才被update，其他字段保持不变。

where和vars负责where语句的生成和绑定参数。

删除：
db.delete('user', where='id=$id', vars={'id':100})

和update类似，不过没有**kw，因为delete只需要where子句。

和Java比，web.py的db操作非常简单，这主要得益于python的**kw参数和内建的dict支持
'''

class DB():
    def __init__(self):
        self.execSQLBatch('mysql -u%s -p%s' % (config.DB_USER, config.DB_PASSWD), 'source ' + config.INIT_DEV_ENV, "Init Environment", "Error occurred while initializing development environment")
        self.execSQLBatch('mysql -u%s -p%s' % (config.DB_USER, config.DB_PASSWD), 'source ' + config.INIT_TABLES, "Init Tables", "Error occurred while initializing development environment")
        self._MASTER = web.database(
            dbn = config.DB_MASTER_TYPE,
            host = config.DB_MASTER_HOST,
            db = config.DB_MASTER_DBNAME,
            user = config.DB_MASTER_USER,
            pw = config.DB_MASTER_PASSWD
        )

        self._SLAVE = web.database(
            dbn = config.DB_SLAVE_TYPE,
            host = config.DB_SLAVE_HOST,
            db = config.DB_SLAVE_DBNAME,
            user = config.DB_SLAVE_USER,
            pw = config.DB_SLAVE_PASSWD
        )
        
    
    def execSQLBatch(self, cmd, subCmd, debugTag, errorTag):
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
            output = process.communicate(subCmd)
            MBLogger.debug("%s ... %s" % (debugTag, output[0]))
            if (output[1]):
                MBLogger.error("%s ... %s" % (errorTag, output[1]))
        except:
            MBLogger.error("Error occurred while executing the sql batch ...", exc_info=True)
            
    def query(self, sql_query, sql_vars=None, processed=False, _test=False):
        return self._MASTER.query(sql_query=sql_query, vars=sql_vars, processed=processed, _test=_test)
            
    def select(self, tables, sql_vars=None, what='*', where=None, order=None, group=None, 
               limit=None, offset=None, _test=False):
        return self._MASTER.select(tables=tables, vars=sql_vars, what=what, where=where, order=order, group=group, 
               limit=limit, offset=offset, _test=_test)
        
    def insert(self, tablename, seqname=None, _test=False, **values):
        return self._MASTER.insert(tablename=tablename, seqname=seqname, _test=_test, **values)
    
    def multiple_insert(self, tablename, values, seqname=None, _test=False):
        return self._MASTER.multiple_insert(tablename=tablename, values=values, seqname=seqname, _test=_test)
    
    def update(self, tables, where, sql_vars=None, _test=False, **values):
        return self._MASTER.update(tables=tables, where=where, vars=sql_vars, _test=_test, **values)
    
    def delete(self, table, where, using=None, sql_vars=None, _test=False):
        return self._MASTER.delete(table=table, where=where, using=using, vars=sql_vars, _test=_test)
    
MBDB = DB()
