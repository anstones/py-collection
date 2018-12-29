# -*- coding: utf-8 -*-
import scrapy,json
import time,random
from ..items import ItjuziItem


class ItjuziSpider(scrapy.Spider):
    name = "itjuzi"
    allowed_domains = ["itjuzi.com"]
    base_url = 'https://www.itjuzi.com/api/companies/{}?type=basic'
    start_urls = []
    for i in range(1, 33632183):
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
            yield scrapy.Request(url=url,callback=self.parse,headers=self.headers,cookies=self.cookies)
            time.sleep(random.random())

    def parse(self, response):
        if response.status == 200:
            item = ItjuziItem()
            item['company_id'] = int(response.url.split('companies/')[-1].split('?')[0])
            # 1.公司简介
            data = json.loads(response.text)
            item['company_name'] = data['data']['basic']['com_name']
            item['company_slogan'] = data['data']['basic']['com_slogan']
            item['company_link'] = data['data']['basic']['com_url']
            item['company_local'] = data['data']['basic']['com_local']
            tag_list = []
            tag_list.append(data['data']['basic']['com_scope']['cat_name'])
            for tag in data['data']['basic']['tag_info']['normal_tag']:
                tag_list.append(tag['name'])
            for tag in data['data']['basic']['tag_info']['especial_tag']:
                tag_list.append(tag['name'])
            item['company_tags'] = tag_list

            # 2.公司基本信息
            item['company_info'] = data['data']['basic']['com_des']
            item['company_full_name'] = data['data']['basic']['com_registered_name']
            item['create_time'] = str(data['data']['basic']['com_born_year'])+'-'+str(data['data']['basic']['com_born_month'])
            item['company_size'] = data['data']['basic']['company_scale']['com_scale_name']
            item['company_status'] = data['data']['basic']['com_status_name']+','+data['data']['basic']['com_stage_name']
            print(item)




