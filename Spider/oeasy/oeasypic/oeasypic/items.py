# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OeasypicItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pic_url = scrapy.Field()
    uid = scrapy.Field()
    image_path = scrapy.Field()
    vid = scrapy.Field()
    insert_time = scrapy.Field()
    id_code = scrapy.Field()
    telephone = scrapy.Field()