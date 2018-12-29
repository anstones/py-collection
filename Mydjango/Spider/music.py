# -*- coding:utf-8 -*-

import base64
import json
import random
import time
import requests
import pymysql
from Crypto.Cipher import AES


class music:

    # 初始化
    def __init__(self):
        config = {
            "host": "127.0.0.1",
            "user": "root",
            "password": "mysql",
            "database": "mine"
        }
        # 数据库操作
        self.db = pymysql.connect(**config)
        self.cursor = self.db.cursor()
        # 设置代理，以防止本地IP被封
        # https
        self.proxy = ['218.25.131.121:47043', '180.118.240.15:808', '182.111.64.7:41766', '27.17.45.90:43411',
                      '222.76.204.110:808',
                      '114.119.116.92:61066', '140.207.50.246:51426', '113.108.242.36:47713', '58.210.136.83:52570',
                      '36.7.128.146:52222',
                      '222.94.147.203:808', '218.76.253.201:61408', '113.105.202.207:3128', '113.105.152.87:41473',
                      '114.225.170.86:53128']
        # http
        # self.proxy = ['123.113.109.20:8118', '61.135.217.7:80', '183.47.40.35:8088', '202.103.12.30:60850', '218.17.253.106:60004',
        #               '119.57.105.73:53281', '60.191.57.78:10800', '114.223.163.70:8118', '116.7.176.75:8118', '118.187.58.34:53281']
        # self.proxy = "  http://202.106.16.36:3128"
        # request headers,这些信息可以在ntesdoor日志request header中找到，copy过来就行
        self.Headers = {
            'Accept': "*/*",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "music.163.com",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"

        }
        self.cookie = {
            ' WM_NIKE': '9ca17ae2e6ffcda170e2e6eeaee53383b685b1d2498d968fa7c15a968a8aaff26bf6879fb2d861b5f0fdd9bb2af0fea7c3b92ab0bdb79ae9689ceeff98e77db78aa8a2d55de9f58d85e550b49fa5ade639a89ffcb0db5f96aac0a9b17ba6b5bda4e552ae8dbad7cd73b2a98296d46af1e8bb85eb47b194baadea7c95f1b78cd85af39aa4d0cd61b4ec8dabc26fa79081bbd662fcb6a4d2f764b2eafd96f03994b6bbaeca34b6bd8497e7648cb1a6afc774b1f5998fea37e2a3',
            ' __root_domain_v': '.163.com',
            ' JSESSIONID-WYYY': 'EIqvjXFiWzamk%2Bf1SmvI9YqMi%2BZAd647dv7oZ7oK25wklZx%5CdQA%2BnMlbVTEhN3nQGVXDZYP8WHK15h%5Cn%5CTqkFlBE6Wqj%5CvqDMQ970ficuc7YHdbTRU8PT6R2SkIomyEBc0v9jQt6eNgt6ABjhaO2n8Y4%5C07U3rI1za5I%5Cg9Ef1XAF9vR%3A1545390089175',
            ' __remember_me': 'true',
            ' __utma': '94650624.884612467.1540450458.1545383069.1545383069.15',
            ' hb_MA-9F44-2FC2BD04228F_source': 'www.baidu.com',
            ' _ga': 'GA1.2.824748388.1544751976',
            ' __utmz': '94650624.1545383069.15.12.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
            ' WM_TID': 'rVGbl32Si%2FFAEABVQBMoOJmIUEDMWhBS',
            ' __f_': '1540952507162',
            ' _ntes_nnid': '28a95982eeb68fc20f682b7c1e84eced,1540450457941',
            ' MUSIC_U': 'e01602495bea77ab5b8bf607fcd70765ffb848c724e20ec26ebb4f4896a42628b140c0332b61734ec8f160b2c2da3f9e376dbffc85054c639463ab0e38077121745e41edd1c07871bf122d59fa1ed6a2',
            'iuqxldmzr_': '32',
            ' _ntes_nuid': '28a95982eeb68fc20f682b7c1e84eced',
            ' __csrf': '3e03ac84c4331fedb56f116c92761268',
            ' WM_NI': 'lcyyjlX21wdwuVhAVW%2B%2BCdfDpAkLg3dA4OXUVvpH2qfksCfZnSv6NyrwNuQb38udhMsLvLkpW%2FykUR1Fl%2FNkp4CJCeePOZWj8jl1thr63um3PjuMK8vcLvdhHojNDxs%2BWnk%3D',
            ' _qddaz': 'QD.q0snlg.st6mi5.jpndfwrz'
        }

    def get_total(self,url):
        response = requests.get(url, headers=self.Headers, cookies=self.cookie)
        content = response.text
        json_obj = json.loads(content)
        total = json_obj.get('total', 0)
        return total

    def get_json(self,url):
        response = requests.get(url, headers=self.Headers, cookies=self.cookie, proxies={'https://': random.choice(self.proxy)})

        content = response.text
        json_obj = json.loads(content)
        # json_dict = json_obj.get('comments', '')
        return json_obj

    def get_allcomments(self, url):
        comments_num = int(self.get_total(url))
        present_page = 0
        if comments_num % 20 == 0:
            page = comments_num / 20
        else:
            page = int(comments_num / 20) + 1
        print("共有%d页评论" % page)
        print("共有%d条评论" % comments_num)
        for i in range(page):
            page_url = url + '?offset={}&limit=20'.format(str(i))
            json_obj = self.get_json(page_url)
            node_list = json_obj.get('comments')
            print(node_list)
            for node in node_list:
                time_local = time.localtime(int(node['time'] / 1000))  # 将毫秒级时间转换为日期
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                nickname = node['user']['nickname']
                avatarUrl = node['user']['avatarUrl']
                userId = str(node['user']['userId'])
                up_date = dt
                content = node["content"].strip()
                commentId = str(node["commentId"])
                likedcount = node["likedCount"]
                params = [nickname, avatarUrl, userId, up_date, content, commentId, likedcount]
                # count = self.cherk_count(commentId)
                # if count <= 1:
                self.cursor.execute(
                    "insert ignore into music126(nickname,avatarUrl,userId,up_date,content,commentId,likedcount) values(%s,%s,%s,%s,%s,%s,%s)",
                    params)
                self.db.commit()

            print("第%d页抓取完毕" % (i+1))
            time.sleep(random.randint(3, 5))

        self.cursor.close()
        self.db.close()

mail = music()
# https://music.163.com/api/v1/resource/comments/R_SO_4_553755659?offset=0&limit=20
mail.get_allcomments("https://music.163.com/api/v1/resource/comments/R_SO_4_553755659")
# mail.get_total('https://music.163.com/api/v1/resource/comments/R_SO_4_553755659')

# CREATE TABLE `music126` (
#   `id` int(20) NOT NULL AUTO_INCREMENT,
#   `nickname` varchar(40) DEFAULT NULL COMMENT '昵称',
#   `avatarUrl` varchar(100) DEFAULT NULL COMMENT '用户头像',
#   `userId` varchar(20) DEFAULT NULL COMMENT '用户id',
#   `up_date` datetime DEFAULT NULL COMMENT '评论时间',
#   `content` varchar(600) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '评论',
#   `commentId` varchar(20) DEFAULT NULL COMMENT '评论id',
#   `likedcount` int(20) DEFAULT NULL COMMENT '点赞数',
#   PRIMARY KEY (`id`),
#   UNIQUE KEY (`commentId`) USING BTREE
# ) ENGINE=InnoDB AUTO_INCREMENT=42331 DEFAULT CHARSET=utf8;
