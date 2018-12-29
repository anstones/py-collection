# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItjuziItem(scrapy.Item):
    # 1.公司简介
    company_name = scrapy.Field()
    company_slogan = scrapy.Field()
    company_link = scrapy.Field()
    company_tags = scrapy.Field()
    company_local = scrapy.Field()

    # 2.公司基本信息
    company_info = scrapy.Field()
    company_full_name = scrapy.Field()
    create_time = scrapy.Field()
    company_size = scrapy.Field()
    company_status = scrapy.Field()

    # 3. 融资
    invest_list = scrapy.Field()
    # 4. 团队信息
    team_list = scrapy.Field()
    # 5. 产品信息
    product_list = scrapy.Field()

    company_id = scrapy.Field()

    # 数据源
    data_source = scrapy.Field()
    data_time = scrapy.Field()
