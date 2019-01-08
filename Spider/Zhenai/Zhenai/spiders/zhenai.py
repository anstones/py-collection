# -*- coding: utf-8 -*-
import scrapy
import json


class ZhenaiSpider(scrapy.Spider):
    name = 'zhenai'
    allowed_domains = ['zhenai.com']
    start_urls = ['http://profile.zhenai.com/v2/follow/ajax.do?type=0&']

    def start_requests(self):
        for i in range(1,15):
            url = self.start_urls[0] + '?page=' + str(i)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        content_str = response.text
        print(content_str)
