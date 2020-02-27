# /usr/bin/env python
# coding=utf8
import urllib2
import urllib
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Articles(object):
    key='XqZJTh9o7kb8'
    sites='http://aff.amigatoy.com'
    saveurl=sites+'/caiji/save'
    verifyurl=sites+'/caiji/verify'
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    def __init__(self):
        pass
    def savearticle(self,title,content,keyword,url):
        postdata = dict(title=title, content=content, keyword=keyword,url=url,key=self.key)
        # logging.warning('postdata is %s' % postdata)
        postdata = urllib.urlencode(postdata)

        # enable cookie
        request = urllib2.Request(self.saveurl, postdata,headers=self.hdr)
        response = urllib2.urlopen(request)
        return response.read()

    def verify(self,url):
        postdata = dict(url=url, key=self.key)
        postdata = urllib.urlencode(postdata)
        logging.warning('url is %s'%self.verifyurl)
        logging.info(postdata)
        request = urllib2.Request(self.verifyurl, postdata,headers=self.hdr)
        response = urllib2.urlopen(request)
        return response.read()




