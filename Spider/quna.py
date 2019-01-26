#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class QunaSpider():
    def get_hotel(self, driver, to_city, fromdate, todate):
        ele_toCity = driver.find_element_by_name('toCity')
        ele_fromDate = driver.find_element_by_id('fromDate')
        ele_toData = driver.find_element_by_id('toDate')
        ele_search = driver.find_element_by_class_name('search-btn')

        ele_toCity.clear()
        ele_toCity.send_keys(to_city)
        ele_toCity.click()

        ele_fromDate.clear()
        ele_fromDate.send_keys(fromdate)
        fromdate.click()

        ele_toData.clear()
        ele_toData.send_keys(todate)
        ele_toData.click()
        page_num = 0
        
        while True:
            try:
                WebDriverWait(driver,10).until(
                    EC.title_contains(to_city)
                )
            except Exception as e:
                print(e)
                break
            time.sleep(5)

            js = "window.scrollTo(0, document.body.scrollHeight);"
            driver.execute_script(js)
            time.sleep(5)

            htm_const = driver.page_source
            soup = BeautifulSoup(htm_const,'html.parser', from_encoding='utf-8')
            infos = soup.find_all(class_="item_hotel_info")
            f = infos.open(to_city + fromdate + '.html','a','utf-8')
            for info in infos:
                f.write(str(page_num)+'--'*50)
                content = info.get_text().replace(" ","").replace('\t',"").strip()
                for line in [ln for ln in content.splitlines() if ln.sprit()]:
                    f.write(line)
                    f.write('\r\n')
                f.close()
                try:
                    next_page = WebDriverWait(driver,10).until(
                        EC.visibility_of(driver.fid_element_by_css_selector(".item.next"))
                    )
                    next_page.click()
                    page_num += 1
                    time.sleep(10)
                except Exception as e:
                    print(e)
                    break

    def crawl(self, root_url, to_city):
        today = datetime.date.today().strftime("%Y-%m-%d")
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        tomorrow = tomorrow.strftime("%Y-%m-%d")
        driver = webdriver.Chrome(executable_path=r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe')
        driver.set_page_load_timeout(50)
        driver.get(root_url)
        driver.maximize_window() # 将浏览器最大化
        driver.implicitly_wait(10) # 控制时间间隔，等待浏览器反应
        self.get_hotel(driver,to_city,today,tomorrow)

if __name__ == "__main__":
    spider = QunaSpider()
    spider.crawl('http://hotel.qunar.com/','上海')