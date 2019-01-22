#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import sys, requests, uuid, hashlib
url = "https://source.unsplash.com/random/800x450"
pic_url = r"C:\\Users\\Administrator\\Desktop\\mine\\python_pic\\"
r = requests.get(url=url)   
url = r.url # 获得真实的图片url
status_code = r.status_code

from urllib.parse import urlparse, parse_qs
parseResult = urlparse(url)
param_dict = parse_qs(parseResult.query) # 解析url中的参数和值

fm = param_dict.get('fm')
pic_extname = None # 图片后缀名
if fm:
    pic_extname = fm[0]

if status_code == 200 and pic_extname:
    # 拼成将要保存的文件名
    filename = str(uuid.uuid1()).replace('-', '') + '.' + pic_extname
    full_filename = pic_url + filename
    file_md5 = None # 文件的md5
    with open(full_filename, 'wb') as file:
        file.write(r.content)
