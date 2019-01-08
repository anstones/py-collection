# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HuxiuItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    write_time= scrapy.Field()
    comment= scrapy.Field()
    favorites= scrapy.Field()
    abstract = scrapy.Field()
