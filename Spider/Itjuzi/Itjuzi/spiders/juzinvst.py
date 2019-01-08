# -*- coding: utf-8 -*-
import scrapy
import json
import time
import random
from ..items import ItjuziItem


class JuziinvstSpider(scrapy.Spider):
    name = 'juziinvst'
    allowed_domains = ['itjuzi.com']
    start_urls = []
    base_url = 'https://www.itjuzi.com/api/companies/{}?type=invst'
    for i in range(1,100):
        start_urls.append(base_url.format(str(i)))
    print(start_urls)

    cookies = {
        'acw_tc': '76b20f4515414969542052363ecd0ef71fef05ee9d9168b3e34d41257d3358',
        'gr_user_id': '74ac15f2-1fe5-4660-ad6d-a7b4a8aba736',
        'gr_session_id_22222-22222-22222-22222': '2e97d178-4899-4c95-b39e-d162a2b6d63d',
        'gr_session_id_22222-22222-22222-22222_2e97d178-4899-4c95-b39e-d162a2b6d63d': 'true',
    }

    headers = {
        'Authorization': 'bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3d3dy5pdGp1emkuY29tL2FwaS9hdXRob3JpemF0aW9ucyIsImlhdCI6MTU0MjE4Mjk1OSwiZXhwIjoxNTQyMTkwMTU5LCJuYmYiOjE1NDIxODI5NTksImp0aSI6InA3MnJQUEt1T0E2TVB1dmciLCJzdWIiOjY2NTM2MSwicHJ2IjoiMjNiZDVjODk0OWY2MDBhZGIzOWU3MDFjNDAwODcyZGI3YTU5NzZmNyJ9.hiXluc0yvFs-9mVFiXdGdcqqZQ79_OZZNqjQLY4i1c0',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.itjuzi.com/company/1',
        'Connection': 'keep-alive',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers, cookies=self.cookies)

    def parse(self, response):
        if response.status == 200:
            item = ItjuziItem()
            item['company_id'] = int(response.url.split('companies/')[-1].split('?')[0])
            data = json.loads(response.text)
            # 3.融资信息
            inv_list = []
            tr_dict = {}
            for invst in data['data']['invst']['acqui_merger_invest']:
                tr_dict['time'] = invst['date']
                tr_dict['round'] = invst['round']
                tr_dict['money'] = invst['money']
                for name in invst['investors']:
                    tr_dict['name'] = name['name']
                    tr_dict['type'] = name['type']
                inv_list.append(tr_dict)
            item['invest_list'] = inv_list
            print(item)
