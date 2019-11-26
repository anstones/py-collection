# coding:utf-8

import time
import json
import os
import requests

from selenium import webdriver
from lib.lconf import Lconf

Global_lconf = Lconf()


class Login():
    def __init__(self,loginurl):
        self.loginurl = loginurl
        
        # self.wait = WebDriverWait(self.browser, 20)

    def save_session(self, session):
        session = json.dumps(session)
        with open('session.txt','w') as f:
            f.write(session)
            print("Cookies have been writed.")

    def load_session(self):
        s = requests.Session()
        with open('session.txt', 'r') as f:
            listcookies = json.loads(f.read())
            for cookie in listcookies:
                s.cookies.set(cookie['name'], cookie['value'])
        return s

    def GetCookies(self):
        # browser = webdriver.Chrome()
        browser = webdriver.Firefox()
        browser.get(self.loginurl)
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/form/label[1]/input[1]').send_keys(Global_lconf.account)
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/form/label[2]/input[1]').send_keys(Global_lconf.passdord)
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/span').click()
        time.sleep(10)
        cookies = browser.get_cookies()
        browser.quit()
        return cookies

    def get_session(self):
        s = requests.Session()
        if not os.path.exists('session.txt'):
            s.headers.clear()
            for cookie in self.GetCookies():
                s.cookies.set(cookie['name'], cookie['value'])
            self.save_session(s)
        else:
            print("**********load session**********")
            s = self.load_session()
        return s

if __name__ == "__main__":
    zhihu = Login('http://upass.10jqka.com.cn/login?act=loginByIframe&isframe=1&view=iwc_quick&redir=http://www.iwencai.com/user/pop-logined')
    session = zhihu.GetCookies()
    zhihu.save_session(session)