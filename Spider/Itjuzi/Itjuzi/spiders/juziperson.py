# -*- coding: utf-8 -*-
import scrapy
import json
import time
import random
from ..items import ItjuziItem

class JuzipersoneSpider(scrapy.Spider):
    name = 'juzipersone'
    allowed_domains = ['itjuzi.com']
    base_url = 'https://www.itjuzi.com/api/companies/{}?type=person'
    start_urls = []
    for i in range(1,33632183):
        start_urls.append(base_url.format(str(i)))

    cookies = {
        'acw_tc': '76b20f4515414969542052363ecd0ef71fef05ee9d9168b3e34d41257d3358',
        'gr_user_id': '74ac15f2-1fe5-4660-ad6d-a7b4a8aba736',
        'gr_session_id_22222-22222-22222-22222': 'f74826a3-4977-4af0-9bc1-f35640fbf358',
        'gr_session_id_22222-22222-22222-22222_f74826a3-4977-4af0-9bc1-f35640fbf358': 'true',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.itjuzi.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'If-None-Match': 'W/^\\^5be41ea0-283d^\\^',
        'If-Modified-Since': 'Thu, 08 Nov 2018 11:31:44 GMT',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers, cookies=self.cookies)
            time.sleep(random.random())

    def parse(self, response):
        if response.status == 200:
            # 解析数据
            item = ItjuziItem()
            item['company_id'] = int(response.url.split('companies/')[-1].split('?')[0])
            data = json.loads(response.text)

            # 4.团队信息
            team_temp_list = []
            for da in data['data']['person']:
                team_dict = {}
                team_dict['name'] = da['name']
                team_dict['position'] = da['des']
                team_dict['info'] = da['per_des']
                team_temp_list.append(team_dict)
                item['team_list'] = team_temp_list
            # 5. 产品信息
            pro_temp_list = []
            for tr in data['data']['products']:
                tr_dict = {}
                tr_dict['name'] = tr['name']
                tr_dict['info'] = tr['des']
                tr_dict['type'] = tr['type_name']
                pro_temp_list.append(tr_dict)
            item['product_list'] = pro_temp_list

            print(item)

