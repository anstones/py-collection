# -*- coding: utf8 -*-

import re
import csv
import json
import time
import traceback
import requests
from lib.lconf import Lconf
from lib.openDay import get_open_day_list
from lib.login import Login
from lib.utils import *

Global_lconf = Lconf()
login = Login(Global_lconf.login_url)

class IWenCai():
    def __init__(self, header):
        self.header = header
        self.url_first = Global_lconf.url_first
        self.url_second = Global_lconf.url_second

    def save_to_csv(self, parms, title, resultList):
        try:
            f = open_file(parms)
            csv_writer = csv.writer(f)
            # title = self._title(title)
            title = ['股票代码', '股票简称', '现价(元)', '涨跌幅(%)', '涨停', '涨停类型', '几天几板', '首次涨停时间', '最终涨停时间', '涨停明细数据', '连续涨停天数(天)', '涨停原因类别', '涨停封单量(股)', '涨停封单额(元)', '涨停封成比(%)2019.10.29', '上市天数(天)2019.11.25']
            csv_writer.writerow(title)
            for result in resultList:
                csv_writer.writerow(result)
            f.close()
        except Exception as e:
            print("error: {}".format(traceback.format_exc()))

    def update_to_csv(self, day, result):
        try:
            parms = "{}日涨停".format(day.replace("-", "月"))
            f = up_file(parms)
            csv_writer = csv.writer(f)
            for i in result:
                csv_writer.writerow(i)
            f.close()
        except Exception as e:
            print("error: {}".format(traceback.format_exc()))

    def _title(self, title):
        new_title = []
        if not isinstance(title, list):
            title = [title]
        for t in title:
            if isinstance(t, str):
                t = t.strip().replace("<br>", "").replace("\\r", "")
                new_title.append(t)
            if type(t) is dict:
                key = list(t.keys())[0]
                new_title.append(key)
        return new_title

    def dosearch(self, day):
        parms = "{}日涨停".format(day.replace("-", "月"))
        # s = login.get_session() # 使用模拟登陆，获取session
        try:
            requestPage = requests.get(self.url_first.format(parms), headers=self.header)
        except Exception as e:
            print("error: {}".format(traceback.format_exc()))
        
        match=re.search(r'allResult = {(.+)};',requestPage.text)
        stockinfo=''
        if match :
            stockinfo = str(match.group(1))
        stocklist="{"
        stocklist += stockinfo
        stocklist += "}"
        stockinfo ="{"+stockinfo+"}"
        decodejson = json.loads(stockinfo)
        total = str(decodejson['total'])
        wccode2hq = [i for i in decodejson['wccode2hq']]
        print('总共有:{}个,分别为:{}'.format(total, wccode2hq))
        title = str(decodejson['title'])
        result = decodejson['result']
        self.save_to_csv(parms, title, result)
        p = is_next(total)
        if p:
            self.getext(day, p)


    def getext(self, day, p):
        token = [Global_lconf.token]
        day = [Global_lconf.day]
        res = dict(zip(day, token))
        for k, v in res.items():
            if k == day:
                requestPage = requests.get(self.url_second.format(v, p), headers=self.header)
                date_list = json.loads(requestPage.text)["result"]
                self.update_to_csv(day, date_list)


def main():
    header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "PHPSESSID=15eebddf09b6c708de7f572cba7a73a2; cid=15eebddf09b6c708de7f572cba7a73a21574734925; ComputerID=15eebddf09b6c708de7f572cba7a73a21574734925; guideState=1; user=MDppY2Fpd2FuZzExMjY6Ok5vbmU6NTAwOjUxMzI5ODU5MTo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxLDQwOzIsMSw0MDszLDEsNDA7NSwxLDQwOzgsMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDEsNDA6Mzo6OjUwMzI5ODU5MToxNTc0NzQ3NzM1Ojo6MTU3NDczNDk4MDo2MDQ4MDA6MDoxMTVmOTk0ODI5MGNmYWQxOWYzMzgwNjA2OTA0OTUxODk6ZGVmYXVsdF8zOjA%3D; userid=503298591; u_name=icaiwang1126; escapename=icaiwang1126; ticket=9d0856d0ecaa20b95d0adbd119323f16; v=ArzBY4zVzZN6IvnPqiRd3eY-jVFttWG_4lR0o5Y-yKeKYVJHvsUwbzJpRCbl",
            "Host": "www.iwencai.com",
            "Referer": "http://www.iwencai.com/",
            "Upgrade-Insecure-Requests": "9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    }

    icai = IWenCai(header)
    open_day_list = get_open_day_list()
    for day in open_day_list:
        icai.dosearch(day)
        time.sleep(Global_lconf.sleep_time)

if __name__ == '__main__':
    main()
