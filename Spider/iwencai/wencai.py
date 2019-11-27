# coding:utf-8

import time
import json
import csv
import random
import traceback
import requests

from selenium import webdriver
from lib.lconf import Lconf
from lib.openDay import get_open_day_list
from lib.constant import HEADER, TITLE, STR, AJAX_HEADER
from lib.utils import *

Global_lconf = Lconf()


class IWenCai():
    def __init__(self):
        self.header = HEADER
        self.header_ajax = AJAX_HEADER
        self.url = Global_lconf.url
        self.url_ajax = Global_lconf.url_ajax
        self.loginurl = Global_lconf.login_url

    def save_session(self, session):
        """ 保存cookie """
        session = json.dumps(session)
        with open('session.txt', 'a+') as f:
            f.write(session)
            print("Cookies have been writed.")

    def load_session(self):
        """ 加载本地保存的cookie """
        s = requests.Session()
        with open('session.txt', 'r') as f:
            listcookies = json.loads(f.read())
            for cookie in listcookies:
                s.cookies.set(cookie['name'], cookie['value'])
        return s

    def GetCookies(self):
        """ 模拟登陆获取cookie """
        browser = webdriver.Chrome()
        browser.get(self.loginurl)
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/form/label[1]/input[1]').send_keys(Global_lconf.account)
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/form/label[2]/input[1]').send_keys(Global_lconf.passdord)
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/span').click()
        time.sleep(2)
        cookies = browser.get_cookies()
        browser.quit()
        return cookies

    def get_session(self):
        """ 获取cookie """
        s = requests.Session()
        try:
            for cookie in self.GetCookies():
                s.cookies.set(cookie['name'], cookie['value'])
        except Exception:
            print("error:{}".format(traceback.format_exc()))
        return s

    def _title(self, title):
        """ 格式化表头 """
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

    def save_to_csv(self, day, results):
        """ 保存到csv文件 """
        try:
            parms = "{}日涨停".format(day.replace("-", "月"))
            f = open_file(parms)
            csv_writer = csv.writer(f)
            csv_writer.writerow(TITLE)
            for result in results:
                csv_writer.writerow(result)
            f.close()
        except Exception:
            print("error: {}".format(traceback.format_exc()))

    def update_to_csv(self, day, results):
        """ 更新csv文件 """
        try:
            parms = "{}日涨停".format(day.replace("-", "月"))
            f = up_file(parms)
            csv_writer = csv.writer(f)
            for i in results:
                csv_writer.writerow(i)
            f.close()
        except Exception:
            print("error: {}".format(traceback.format_exc()))

    def crawl_when(self, url):
        """ 访问被限制，重新获取cookie，抓取页面"""
        try:
            s = self.get_session()
            reqpage = s.get(url, headers=self.header)
            return s, reqpage
        except Exception:
            print("error:{}".format(traceback.format_exc()))

    def crawlpage(self):
        """ 开始抓取页面 """
        s = self.get_session()
        open_day_list = get_open_day_list(params=Global_lconf.params)
        for day in open_day_list:
            parms = "{}日涨停".format(day.replace("-", "月"))
            url = self.url.format(parms)
            try:
                reqpage = s.get(url, headers=self.header)
                data_page = json.loads(reqpage.text)
            except Exception:
                s, reqpage = self.crawl_when(url)
                # print("error:{}".format(traceback.format_exc()))
                print("error: need to relogin")

            status, data = data_page.get("success"), data_page.get("data").get("result")
            if status and data:
                self.parese_paage(s, data, day)

    def get_next(self, s, token, day, p):
        """ 分页抓取除第一页的内容，更新到csv文件 """
        cookie = requests.utils.dict_from_cookiejar(s.cookies)
        for i in range(2, p+1):
            url = self.url_ajax.format(token,  i)
            try:
                print('{}的数据需要分页抓取，正在抓取第{}页'.format(day, i))
                reqpage = requests.get(url, headers=self.header_ajax, cookies=cookie)
            except Exception:
                print("error:{}".format(traceback.format_exc()))
            results = json.loads(reqpage.text)
            results = results["result"]
            self.update_to_csv(day, results)

    def get_next_p(self, s, token, day, p):
        """ 分页抓取除第一页的内容，更新到csv文件 """
        for i in range(2, p+1):
            parms = "{}日涨停".format(day.replace("-", "月")) 
            url = self.url.format(parms) + "&p={}".format(i)
            try:
                print('{}的数据需要分页抓取，正在抓取第{}页'.format(day, i))
                reqpage = s.get(url, headers=self.header)
                data_page = json.loads(reqpage.text)
            except Exception:
                s, reqpage = self.crawl_when(url)
                # print("error:{}".format(traceback.format_exc()))
                print("error: need to relogin")

            status, data = data_page.get("success"), data_page.get("data").get("result")
            if status and data:
                self.parese_paage_p(data, day, i)

    def parese_paage_p(self, data, day, i):
        result = data.get("result")
        self.update_to_csv(day, result)

    def parese_paage(self, s, data, day):
        """ 解析页面内容，判断是否需要分页抓取 """
        token, total = data.get("token"), data.get("total")
        result = data.get("result")
        p = is_next(total)
        print('抓取{}的数据, 总共有:{}个'.format(day, total))
        self.save_to_csv(day, result)

        # 如果当天涨停数量大于70(可以在配置文件中定义，为了减少请求次数，这里设置为最大值)
        # 则需要爬取剩下的内容，追加到文件中
        if p:
            self.get_next_p(s, token, day, p)
        # 短暂睡眠减小压力
        time.sleep(random.randint(2, 5))


def main():
    iwenc = IWenCai()
    # session = iwencai.GetCookies()
    # iwencai.save_session(session)
    iwenc.crawlpage()

if __name__ == "__main__":
    main()
