import urllib.request
import json

"""
获取京东商品价格
"""
def jd_price(url):
    sku = url.split('/')[-1].strip(".html")
    print(sku)
    price_url = "https://p.3.cn/prices/mgets?skuIds=J_" + sku
    response = urllib.request.urlopen(price_url)
    content = response.read()
    result = json.loads(content.decode())
    print(result)
    record = result[0]
    # print "price:", record['p']
    print(record['m'])


if __name__ == "__main__":
    jd_price("https://item.jd.com/12419422058.html")
