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
        self.proxy = ['123.113.109.20:8118']
        # self.proxy = "  http://202.106.16.36:3128"
        # request headers,这些信息可以在ntesdoor日志request header中找到，copy过来就行
        self.Headers = {
            'Accept': "*/*",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "music.163.com",
            'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"

        }
        # # 使用http.cookiejar.CookieJar()创建CookieJar对象
        # self.cjar = http.cookiejar.CookieJar()
        # self.proxy_support = urllib.request.ProxyHandler(self.proxyUrl)
        # # 使用HTTPCookieProcessor创建cookie处理器，并以其为参数构建opener对象
        # self.cookie = urllib.request.HTTPCookieProcessor(self.cjar)
        # self.opener = urllib.request.build_opener(self.cookie, self.proxy_support)
        # # 将opener安装为全局
        # urllib.request.install_opener(self.opener)
        # 第二个参数
        self.second_param = "010001"
        # 第三个参数
        self.third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        # 第四个参数
        self.forth_param = "0CoJUm6Qyw8W8jud"

    def get_params(self, page):
        # 获取encText，也就是params
        iv = "0102030405060708"
        first_key = self.forth_param
        second_key = 'F' * 16
        if page == 0:
            first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
        else:
            offset = str((page - 1) * 20)
            first_param = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' % (offset, 'false')
        self.encText = self.AES_encrypt(first_param, first_key, iv)
        self.encText = self.AES_encrypt(self.encText.decode('utf-8'), second_key, iv)
        return self.encText

    def AES_encrypt(self, text, key, iv):
        # AES加密
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
        encrypt_text = encryptor.encrypt(text.encode('utf-8'))
        encrypt_text = base64.b64encode(encrypt_text)
        return encrypt_text

    def get_encSecKey(self):
        # 获取encSecKey
        encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
        return encSecKey

    def get_json(self, url, params, encSecKey):
        # post所包含的参数
        self.post = {
            'params': params,
            'encSecKey': encSecKey,
        }
        # 对post编码转换
        # self.postData = urllib.parse.urlencode(self.post).encode('utf8')
        # print(self.postData)
        # self.response = ''
        # try:
        # 发出一个请求
        response = requests.post(url, self.post, proxies={'https://': random.choice(self.proxy)}, headers=self.Headers)
        time.sleep(random.randint(1, 3))
        # except Exception as e:
        #     print(e)
        # # 得到响应
        # self.response = urllib.request.urlopen(self.request)
        # # 需要将响应中的内容用read读取出来获得网页代码，网页编码为utf-8
        self.content = response.text
        # # 返回获得的网页内容
        return self.content

    def get_hotcomments(self, url):
        # 获取热门评论
        params = self.get_params(1)
        encSecKey = self.get_encSecKey()
        content = self.get_json(url, params, encSecKey)
        json_dict = json.loads(content)
        hot_comment = json_dict['hotComments']
        f = open('./HotComments.txt', 'w', encoding='utf-8')
        for i in hot_comment:
            # 将评论输出至txt文件中
            time_local = time.localtime(int(i['time'] / 1000))  # 将毫秒级时间转换为日期
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            f.write('用户: ' + i['user']['nickname'] + '\n')
            f.write('点赞数: ' + str(i['likedCount']) + '\n')
            f.write('发表时间: ' + dt + '\n')
            f.write('评论: ' + i['content'] + '\n')
            f.write('-' * 40 + '\n')
        f.close()

    def get_allcomments(self, url):
        # 获取全部评论
        params = self.get_params(1)
        encSecKey = self.get_encSecKey()
        content = self.get_json(url, params, encSecKey)
        print(content)
        json_dict = json.loads(content)
        print(json_dict)
        comments_num = int(json_dict['total'])
        # f = open('./AllComments.txt', 'w', encoding='utf-8')
        present_page = 0
        if (comments_num % 20 == 0):
            page = comments_num / 20
        else:
            page = int(comments_num / 20) + 1
        print("共有%d页评论" % page)
        print("共有%d条评论" % comments_num)
        # 逐页抓取
        for i in range(page):
            params = self.get_params(i + 1)
            encSecKey = self.get_encSecKey()
            json_text = self.get_json(url, params, encSecKey)
            json_dict = json.loads(json_text)
            present_page = present_page + 1
            for i in json_dict['comments']:
                # 将评论输出至txt文件中
                time_local = time.localtime(int(i['time'] / 1000))  # 将毫秒级时间转换为日期
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                nickname = i['user']['nickname']
                avatarUrl = i['user']['avatarUrl']
                userId = str(i['user']['userId'])
                up_date = dt
                content = i["content"].strip()
                commentId = str(i["commentId"])
                likedcount = i["likedCount"]
                params = [nickname, avatarUrl, userId, up_date, content, commentId, likedcount]
                # count = self.cherk_count(commentId)
                # if count <= 1:
                self.cursor.execute(
                    "insert ignore into netmusic126(nickname,avatarUrl,userId,up_date,content,commentId,likedcount) values(%s,%s,%s,%s,%s,%s,%s)",
                    params)
                self.db.commit()

            print("第%d页抓取完毕" % present_page)

        self.cursor.close()
        self.db.close()


mail = music()

# mail.get_hotcomments("https://music.163.com/weapi/v1/resource/comments/R_SO_4_553755659?csrf_token=")
mail.get_allcomments("http://music.163.com/weapi/v1/resource/comments/R_SO_4_553755659?csrf_token=")


# CREATE TABLE `netmusic126` (
#   `id` int(20) NOT NULL AUTO_INCREMENT,
#   `nickname` varchar(40) DEFAULT NULL COMMENT '昵称',
#   `avatarUrl` varchar(100) DEFAULT NULL COMMENT '用户头像',
#   `userId` varchar(20) DEFAULT NULL COMMENT '用户id',
#   `up_date` datetime DEFAULT NULL COMMENT '评论时间',
#   `content` varchar(600) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '评论',
#   `commentId` varchar(20) DEFAULT NULL COMMENT '评论id',
#   `likedcount` int(20) DEFAULT NULL COMMENT '点赞数',
#   PRIMARY KEY (`id`),
#   UNIQUE KEY `index_id` (`commentId`) USING BTREE
# ) ENGINE=InnoDB AUTO_INCREMENT=42331 DEFAULT CHARSET=utf8;
