# -*- coding: utf-8 -*-
import scrapy
import simplejson
from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
import logging

import json

from moborg.classes.articles import Articles
from moborg.items import MoborgItem


class ActionsSpider(CrawlSpider):
    name = 'actions'
    allowed_domains = ['play.mob.org']
    start_urls = ['http://play.mob.org/genre/brodilki_action/']

    rules = (
        Rule(LinkExtractor(allow=r'http:\/\/play\.mob\.org\/genre\/brodilki_action\/page-\d+/',
                           restrict_xpaths=('/html/body/div[1]/div[2]/div[1]/div/div[2]/div[20]'), ),
             callback='parse_item', follow=True),
    )


     #取列表
    def parse_item(self, response):
        urls=Selector(response=response).xpath('//div[@class="game-item"]/div[@class="summary"]/div[@class="info-block"]/div[@class="title"]/a/@href').extract()
        logging.warning("urls is %s"%urls)
        if urls:#如果列表不为空
            for i in range(len(urls)):
                yield scrapy.Request(url=urls[i],callback=self.parsecontent,errback=self.parseerror)

    #请求内容页面
    def get_items(self,url):
        logging.warning("get url success %s"%url)

        #logging.warning("get response %s"%response)

    #内容页面处理
    def parsecontent(self,response):
        articles = Articles()
        result = articles.verify(response.url)
        objresult = simplejson.loads(result)
        if (objresult['status']):
            logging.warning("start parseconent %s"%response)
            mobitem=MoborgItem()
            mobitem['name']=response.xpath('//span[@itemprop="name"]/text()').extract()
            mobitem['imagelist']=response.xpath('//div[@class="screenshots"]/node()').extract()
            mobitem['content']=response.xpath('//div[@itemprop="description"]/text()').extract()
            mobitem['url']=response.url
            logging.warning("get imagelist is %s" % mobitem['imagelist'])
            logging.warning("get content is %s" % mobitem['content'])

            return mobitem



    def parseerror(self,response):
         logging.warning("get url error %s" % response.url)


