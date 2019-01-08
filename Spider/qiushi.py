import json
import requests
from lxml import etree

"""
糗事百科爬虫
"""
class QiuShi():
    def __init__(self):
        self.base_url = "https://www.qiushibaike.com/text/page/{}"
        # https://www.qiushibaike.com/users/17535149/page_2/
        self.start_url = []
        self.file = open('./qiushi.json', 'w')
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/69.0.3497.100 Safari/537.36 "
        }

    def gen_url(self):
        self.start_url = [self.base_url.format(i) for i in range(1, 14)]

    def get_page(self, url):
        page = requests.get(url, headers=self.header)
        html = page.content
        return html

    def get_link(self,link):
        page = requests.get(link,headers=self.header)

    def parse_page(self, data):
        html = etree.HTML(data)
        node_list = html.xpath('//*[@id="content-left"]/div')
        data_list = []
        for node in node_list:

            temp = {}
            name = node.xpath("./div[1]/a[2]/h2/text()")
            if len(name) > 0:
                temp["name"] = name[0].strip()
            else:
                temp["name"] = "匿名用户"

            good = node.xpath("./div[2]/span[1]/i/text()")
            if len(good) > 0:
                temp["good"] = good[0].strip()
            else:
                temp["good"] = 0

            number = node.xpath("./div[2]/span[2]/a/i/text()")
            if len(number) > 0:
                temp["number"] = number[0].strip()
            else:
                temp["number"] = 0
            link = node.xpath("./div[1]/a[2]/@href")
            if len(link) > 0:
                temp["link"] = "https://www.qiushibaike.com"+link[0].strip()
            else:
                temp["link"] = "匿名"
            temp["content"] = "".join(node.xpath("./a[1]/div/span[1]/text()")).strip()
            data_list.append(temp)
        return data_list

    def save(self, content):
        for line in content:
            str_data = json.dumps(line, ensure_ascii=False) + ",\n"
            self.file.write(str_data)

    def __del__(self):
        self.file.close()

    def main(self):
        self.gen_url()
        for i in self.start_url:
            data = self.get_page(i)
            content = self.parse_page(data)
            self.save(content)


if __name__ == '__main__':
    qiushi = QiuShi()
    qiushi.main()
