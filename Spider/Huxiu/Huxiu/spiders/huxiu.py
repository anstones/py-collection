# -*- coding: utf-8 -*-
import scrapy
import json,time,random
from pyquery import PyQuery as pq
from ..items import HuxiuItem

class HuxiuSpider(scrapy.Spider):
    name = 'huxiu'
    allowed_domains = ['huxiu.com']
    start_urls = ['https://www.huxiu.com/v2_action/article_list']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    def start_requests(self):
        for i in range(1, 2012):
            url = self.start_urls[0] + '?page=' + str(i)
            time.sleep(random.random())
            yield scrapy.Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response):

        content_str = response.text
        content = json.loads(content_str)["data"]
        doc = pq(content)
        lis = doc('.mod-art').items()
        for ite in lis:
            item = HuxiuItem()
            item["title"] = ite('.msubstr-row2').text()
            item["url"]= 'https://www.huxiu.com' + str(ite('.msubstr-row2').attr('href')),
            item["name"] = ite('.author-name').text(),
            item["write_time"] = ite('.time').text(),
            item["comment"]= ite('.icon-cmt+ em').text(),
            item["favorites"]= ite('.icon-fvr+ em').text(),
            item["abstract"]=ite('.mob-sub').text()
            print(item)
            yield item

