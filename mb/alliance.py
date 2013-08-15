# -*- coding: utf-8 -*-
'''
Created on Aug 13, 2013

@author: Carl, Aaron
'''

import time
import urllib
import urllib2
import base64
import hashlib
import hmac
import uuid
from mb.logger import MBLogger

_OAUTH_SIGN_METHOD = 'HMAC-SHA1'
_OAUTH_VERSION = '1.0'
_OAUTH_TOKEN = 'openyiqifa'

class YiqifaAPI(object):

    baseUrl = "http://openapi.yiqifa.com/api2"
    dataFormat = "json"
    apiVersion = "2.0"
    consumerKey = None
    consumerSecret = None

    def __init__(self, key, secret):
        self.consumerKey = key
        self.consumerSecret = secret

    def call(self, req):
        #获取业务参数
        apiParams = req.getAPIParam()
        
        reqUrl = "%s/%s.%s?" % (self.baseUrl, req.getMethodName(), self.dataFormat)
        paramStr = self.encodeParams('&', apiParams)
        reqUrl = "%s%s" % (reqUrl, paramStr)

        #发起请求
        r = self.httpCall(reqUrl, self.consumerKey, self.consumerSecret)

        #解析结果
        if r:
            #处理中文编码
            return r.decode('GBK').encode('utf-8')
        return ''

    def httpCall(self, reqUrl, key, secret):
        au = self.genOauth(reqUrl, key, secret)
        req = urllib2.Request(reqUrl, data=None)
        if au:
            req.add_header('Authorization', au)
        resp = None
        respData = None
        try:
            resp = urllib2.urlopen(req)
            respData = resp.read()
        except:
            MBLogger.error("Error occurred while sending http request to Alliance...", exc_info=True)
        finally:
            if resp:
                resp.close()
        return respData

    def genOauth(self, reqUrl, key, secret):
        authParams = self.genAuthParams(key, secret)
        mergeParams = dict()
        mergeParams.update(authParams)
        mergeParams.update(self.parseGetParams(reqUrl))
        baseStr = self.genBaseStr(reqUrl, mergeParams)
        tk = "%s&%s" % (secret, _OAUTH_TOKEN)
        sign = self.genSign(tk, baseStr)
        return "OAuth %s, oauth_signature=\"%s\"" % (self.encodeParams(',', authParams, True), sign)


    def genSign(self, key, data):
        return self.quoteStr(base64.b64encode(hmac.new(key, data, hashlib.sha1).digest()))

    def genBaseStr(self, reqUrl, authParams):
        return "GET&%s&%s" % (self.getBaseReqUrl(reqUrl), self.encodeBaseParams(authParams))

    def getBaseReqUrl(self, reqUrl):
        n = reqUrl.find('?')
        if n > 0:
            return reqUrl[:n]
        return reqUrl

    def parseGetParams(self, reqUrl):
        d = dict()
        i = reqUrl.find('?')
        if i > 0:
            reqUrl = reqUrl[i+1:]
        for s in reqUrl.split('&'):
            n = s.find('=')
            if n > 0:
                key = s[:n]
                value = urllib.unquote(s[n+1:])
                d[key] = value.decode('utf-8')
        return d;

    def genAuthParams(self, key, secret):
        return dict( \
            oauth_consumer_key=key, \
            oauth_signature_method=_OAUTH_SIGN_METHOD, \
            oauth_nonce=self.genNonce(), \
            oauth_timestamp=str(int(time.time())), \
            oauth_version=_OAUTH_VERSION, \
            oauth_token=_OAUTH_TOKEN)

    def genNonce(self):
        return uuid.uuid4().hex

    def encodeParams(self, joinStr, kw, quoteValue=False):
        if kw:
            args = []
            for k, v in kw.iteritems():
                qv = v.encode('utf-8') if isinstance(v, unicode) else str(v)
                args.append(('%s=\"%s\"' % (k, self.quoteStr(qv))) if quoteValue else ('%s=%s' % (k, self.quoteStr(qv))))
            return joinStr.join(args)
        return ''
    
    def encodeBaseParams(self, kw):
        if kw:
            baseEncodeStr = None
            for k, v in kw.iteritems():
                qv = v.encode('utf-8') if isinstance(v, unicode) else str(v)
                if baseEncodeStr:
                    baseEncodeStr = "%s%s%s%s%s" % (baseEncodeStr, "%26", k, "%3D", self.quoteStr(qv))
                else:
                    baseEncodeStr = "%s%s%s" % (k, "%3D", self.quoteStr(qv))
            return baseEncodeStr
        return ''
    
    def quoteStr(self, s):
        if isinstance (s, unicode):
            s = s.encode('utf-8')
        return urllib.quote(str(s), safe='')

#############具体API对应的Request类###############

class WebsiteCategoryReqeust(object):
    
    fields = None
    type = None
    methodName = "open.website.category.get"
    
    def __init__(self, fields, siteType):
        self.fields = fields
        self.type = siteType
    
    def getMethodName(self):
        return self.methodName
    
    def getAPIParam(self):
        return dict( \
            fields=self.fields, \
            type=self.type)

class WebsiteListRequest(object):

    catId = None
    fields = None
    type = None
    methodName = "open.website.list.get"

    def __init__(self, fields, siteType, catId):
        self.catId = catId
        self.fields = fields
        self.type = siteType
    
    def getMethodName(self):
        return self.methodName

    def getAPIParam(self):
        return dict( \
            catId=self.catId, \
            fields=self.fields, \
            type=self.type)
