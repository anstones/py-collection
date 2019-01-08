#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import requests
import random
from lxml import etree
import json
import time
import pymysql
import urllib3
urllib3.disable_warnings()
import re

class CreateDB():
    def __init__(self):
        self.config = {
                "host": "192.168.6.187",
                "user": "root",
                "password": "mysql",
                "database": "mine"
            }
        # 数据库
        self.db = pymysql.connect(**self.config)
        self.cursor = self.db.cursor()
        self.table_name = 'proxy'

    def table_exists(self):
        sql = "show tables;"
        self.cursor.execute(sql)
        tables = [self.cursor.fetchall()]
        table_list = re.findall('(\'.*?\')',str(tables))
        table_list = [re.sub("'",'',each) for each in table_list]
        if self.table_name in table_list:
            return 1
        else:
            return 0
    
    def _create(self):
        sql = "CREATE TABLE `{}` (`id` int(20) NOT NULL AUTO_INCREMENT,`ip_port` varchar(40) DEFAULT NULL COMMENT 'ip端口',`ip_area` varchar(40) DEFAULT NULL COMMENT 'IP地址',`socket_type` varchar(20) DEFAULT NULL COMMENT 'http类型',`sped` varchar(20) DEFAULT NULL COMMENT '速度',`link_sped` varchar(20) DEFAULT NULL COMMENT '连接速度',`validity` varchar(20) DEFAULT NULL COMMENT '有效期',`validate` varchar(20) DEFAULT NULL COMMENT '测试时间',PRIMARY KEY (`id`),UNIQUE KEY (`ip_port`) USING BTREE)ENGINE=InnoDB AUTO_INCREMENT=42331 DEFAULT CHARSET=utf8;".format(self.table_name)
        try:
            self.cursor.execute(sql)
            self.db.commit
        except Exception as e:
            print(e)
            
    def cre_db(self):
        # 建表
        num = self.table_exists()
        if num != 1:
            self._create()
        else:
            sql = "drop database if exists `{}`".format(self.table_name)
            self.cursor.execute(sql)
            self.db.commit()
            self._create()

    
class MyProxy():
    def __init__(self, socket_type):
        # 代理ip
        self.proxy = ['218.25.131.121:47043', '180.118.240.15:808', '182.111.64.7:41766', '27.17.45.90:43411','222.76.204.110:808',
                      '114.119.116.92:61066', '140.207.50.246:51426', '113.108.242.36:47713', '58.210.136.83:52570',
                      '36.7.128.146:52222',
                      '222.94.147.203:808', '218.76.253.201:61408', '113.105.202.207:3128', '113.105.152.87:41473',
                      '114.225.170.86:53128']
        self.url_list = []
        self.base_url = 'https://www.xicidaili.com/%s/{}'%(socket_type)
        self.header = {
            'Referer': 'https://www.xicidaili.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        self.web_cookies = 'free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTczODYyZDIzN2JiZWFkY2RjMTQyMzNhOGM4Yzk5ZWYzBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUQxVHJRdW45YnEzb3o3bkpCMDFGV2E3WEdxWlpzOUs4WkVmTTFhN01XaEk9BjsARg%3D%3D--e7b6b828c8a22ae6159eefeb423caef1dc464eef; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1545381793,1545630460; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1545631053'
        self.cookies = self.get_cookie(self.web_cookies)
        self.file = open('./proxy_{}.json'.format(socket_type), 'w')

        self.config = {
            "host": "192.168.6.187",
            "user": "root",
            "password": "mysql",
            "database": "mine"
        }
        # 数据库
        self.db = pymysql.connect(**self.config)
        self.cursor = self.db.cursor()

    def get_cookie(self, cookies):
        cookie = {}
        for line in cookies.split(';'):
            key, value = line.split('=', 1)
            cookie[key] = value
        return cookie

    def gen_url(self):
        # 提取前100页的有效ip
        self.url_list = [self.base_url.format(i) for i in range(1, 151)]

    def get_page(self, url):
        page = requests.get(url, cookies=self.cookies, headers=self.header, proxies={'https://': random.choice(self.proxy)}, verify=False)
        time.sleep(random.randint(1, 3))
        return page.content

    def parse_data(self, data):
        html = etree.HTML(data)
        node_list = html.xpath('//*[@id="ip_list"]/tr')
        # print(len(node_list))
        data_list = []
        for node in node_list:
            temp = {}
            try:
                ip = node.xpath('./td[2]/text()')[0] if len(node.xpath('./td[2]/text()')) >= 1 else ''
                port = node.xpath('./td[3]/text()')[0] if len(node.xpath('./td[3]/text()')) >= 1 else ''
                temp['ip_port'] = ip + ":" + port
                temp['ip_area'] = node.xpath('./td[4]/a/text()')[0] if len(node.xpath('./td[4]/a/text()')) >= 1 else ''
                temp['socket_type'] = node.xpath('./td[6]/text()')[0] if len(node.xpath('./td[6]/text()')) >= 1 else ''
                temp['sped'] = node.xpath('./td[7]/div/@title')[0] if len(node.xpath('./td[7]/div/@title')) >= 1 else ''
                temp['link_sped'] = node.xpath('./td[7]/div/@title')[0] if len(node.xpath('./td[8]/div/@title')) >= 1 else ''
                # 有效期以分钟为单位的ip 抛弃
                validity = node.xpath('./td[9]/text()')[0] if len(node.xpath('./td[9]/text()')) >= 1 else ''
                if '分钟'in validity:
                    temp['validity'] = ''
                else:
                    temp['validity'] = validity

                temp['validate'] = node.xpath('./td[10]/text()')[0] if len(node.xpath('./td[10]/text()')) >= 1 else ''

            except Exception as e:
                print(e)

            if temp['validity'] != '':
                data_list.append(temp)

        return data_list

    def save(self, content):
        for line in content:
            str_data = json.dumps(line, ensure_ascii=False) + ",\n"
            self.file.write(str_data)

    def to_db(self, data_list):
        for data in data_list:
            data_obj = data
            if data_obj:
                params = list(data_obj.values())
                # params = [ip_port, ip_area, socket_type, sped, link_sped, validity, validate]
                self.cursor.execute(
                    "insert ignore into proxy(ip_port, ip_area, socket_type, sped, link_sped, validity, validate) values(%s, %s, %s, %s, %s, %s, %s)", params)

                self.db.commit()

    def __del__(self):
        self.file.close()

    def main(self):
        createdb = CreateDB()
        createdb.cre_db()

        self.gen_url()
        for url in self.url_list:
            page = p.get_page(url)
            p.parse_data(page)
            content = p.parse_data(page)
            p.to_db(content)


if __name__ == '__main__':
    socket_type = input('请输入需要的网络请求类型[http/https]:')
    if socket_type == 'http':
        p = MyProxy('wt')
    elif socket_type == 'https':
        p = MyProxy('wn')
    else:
        print('输入错误:[http/https]')
    p.main()
