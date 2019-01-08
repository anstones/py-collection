# -*- coding: utf-8 -*-
import time
import scrapy
import json
from ..items import OeasypicItem


image_path = "/home/oeasy/Desktop/Mydjango/oeasy/images/"


class OeasyPicSpider(scrapy.Spider):
    name = 'oeasy_pic'
    allowed_domains = ['0easy.com']
    # start_urls = ["http://bigdata.0easy.com/yihao01-bigdata-search/search/door/searchDoorRecord.do"]
    start_urls = ['http://bigdata.0easy.com/yihao01-bigdata-search/search/door/searchDoorRecord.do']
    #
    cookie = {'TOKEN': '3880650844fdbdf0e7a371d1ae05060e_3a8a7b67244d4f869a3f5fef9118b7f8', 'eid01': 'ymhmG1wTFIxUzwPcNXo1Ag==', 'JSESSIONID': 'A95A82A956D1E25779CAE6CEF71A05DF'}
    headers = {
        'Connection': 'keep - alive',  # 保持链接状态
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
        # "Referer": "http://bigdata.0easy.com/yihao01-bigdata-search/community_entrance.jsp?unit_id=2033"
    }

    def start_requests(self):
        url = self.start_urls[0]
        for i in range(1,126750):
        # for i in range(1, 2):
            params = {
                "unit_id": "2033",
                "pageSize": "10",
                "pageNo": str(i)
            }
            print("正爬取第{}页".format(i))
            time.sleep(1)
            yield scrapy.FormRequest(url, callback=self.parse, formdata=params, headers=self.headers, cookies=self.cookie)

    def parse(self, response):
        data_list = json.loads(response.text)['items']
        for node in data_list:
            item = OeasypicItem()
            item["name"] = node["user_name"]
            pic = node["picurl"]
            if "," in pic:
                pic_url = pic.split(",")[0]
                item["pic_url"] = "https://qimg.0easy.com/" + pic_url
            else:
                item["pic_url"] = "https://qimg.0easy.com/" + pic
            # item["uid"] = node["uid"]
            # item["vid"] = node["vid"]
            # item["insert_time"] = node["insert_time"]
            item["id_code"] = node["id_code"]
            item["telephone"] = node["telephone"]
            # self.save_pic(item["pic_url"], item["name"], item["insert_time"])
            print(item)
            yield item

    import requests
    from PIL import Image
    from io import BytesIO
    # def save_pic(self, url, name, insert_time):
    #     response = requests.get(url)
    #     image = Image.open(BytesIO(response.content))
    #     image.save(image_path + name +'.jpg')
