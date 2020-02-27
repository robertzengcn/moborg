# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from moborg.classes.articles import Articles
from moborg.classes.baitrans import Baitrans

from bs4 import BeautifulSoup
import logging


class MoborgPipeline(object):
    def process_item(self, item, spider):
        contents = ''
        contents = contents.join(item['imagelist'])
        logging.warning("current imglist is %s"%contents)
        soup = BeautifulSoup(contents.encode('utf-8'))
        imglist=''
        for t in soup.find_all("img"):  # the actual selection depends on your specific code
            src = t.get('src')
            if src:
                imglist+='<img src="'+src+'"/></br>'

        logging.warning("imglist is %s"%imglist)
        baitran=Baitrans()
        logging.warning("trans name is %s" % item['name'][0].encode('utf-8'))
        itemnames = baitran.tran(item['name'][0].encode('utf-8'), 'en', 'zh')
        needtrans=baitran.removehtml(item['content'][0].encode('utf-8'))
        needtrans = baitran.tran(needtrans,'en','zh')
        allcontent=imglist+ needtrans
        logging.warning("get content is %s" % allcontent)
        articles=Articles()
        logging.warning("result name is %s"%itemnames)
        logging.warning("result content is %s" %allcontent)
        articles.savearticle(itemnames,allcontent,'action_game',item['url'])

        return item
