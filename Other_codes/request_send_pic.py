#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
from io import BytesIO

url = 'http://192.168.6.12:5050/person_detect'

files = {'img':('20190428174541.jpg', open('./20190428174541.jpg', 'rb'), 'image/png', {})}

num = requests.post(url=url, data={'type':'1'}, files=files)

print(num.text)


# tornado reques获取form_data 图片参数
imgfile = self.request.files.get('img')[0]   
# 存储为内存流格式（bytes类型）
img = BytesIO(imgfile['body']).read()