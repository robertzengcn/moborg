# /usr/bin/env python
# coding=utf8

import httplib
import md5
import urllib
import random
import logging
import json
import re


class Baitrans(object):
    def __init__(self):
        pass

    appid = '20170812000072047'
    secretKey = 'WAhi0Ns8pohAcXINHP_4'
    httpClient = None
    myurl = '/api/trans/vip/translate'

    def tran(self, q, fromLang, toLang):
        salt = random.randint(32768, 65536)
        sign = self.appid + q + str(salt) + self.secretKey
        m1 = md5.new()
        m1.update(sign)
        sign = m1.hexdigest()
        myurl = self.myurl + '?appid=' + self.appid + '&q=' + urllib.quote(
            q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

        try:
            httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)

            # response是HTTPResponse对象
            response = httpClient.getresponse()
            result=response.read()
            #logging.warning("trans result %s"%result['trans_result'])
            #print result
            objresult=json.loads(result)
            #print objresult['trans_result'][0]['dst']
            resultstr=""
            #print '222'
            #print objresult
            transresult=''
            for index in range(len(objresult['trans_result'])):
                transresult +=objresult['trans_result'][index]['dst']
            logging.warning('transresult is %s'%transresult)
            return transresult
        except Exception, e:
            print e

        finally:
            if httpClient:
                httpClient.close()
    pass
    def removehtml(self,content):
        dr = re.compile(r'<[^>]+>', re.S)
        content = dr.sub('', content)
        return content
    def removescript(self,content):
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script

        return content
