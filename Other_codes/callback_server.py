# -*- encoding: utf-8 -*-

import os
import datetime
import urllib.parse
import json
import requests
import tornado.ioloop
from tornado import web, gen
from concurrent.futures import ThreadPoolExecutor
import traceback
from lib.logger import logger
from lib.utils import *
from lib.common_data import *
from lib.get_cookie import BASE_COOKIE
from lib.tornado_request import TornadoHttpRequest
from core.gconf import GlobalConf
from core.login import Login
from requests_toolbelt import MultipartEncoder

log = Login()
cookie = log.login_cookies("VCM")

header_rel = {}
header_rel['Cookie'] = headers["Cookie"].format(BASE_COOKIE.cookie)

header = {}
header['Cookie'] = headers_download["Cookie"].format(BASE_COOKIE.cookie)

header_up = headers_image
header_up["Cookie"] = headers_image["Cookie"].format(BASE_COOKIE.cookie)

header_upload = headers_upload
header_upload["Cookie"] = headers_upload["Cookie"].format(BASE_COOKIE.cookie)

tornado_request = TornadoHttpRequest(logger=logger)
executor = ThreadPoolExecutor(8)
Global_configure = GlobalConf()

# 获取图片上传通道接口
get_upload_api = 'https://' + Global_configure.vcm_host + Global_configure.get_upload_url
# 发布文件
release_file_api = 'https://' + Global_configure.vcm_host + Global_configure.release_file_url

class CallBackHandler(web.RequestHandler):

    def set_default_headers(self):        
        self.set_header("Access-Control-Allow-Origin", "*")        
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")        
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @gen.coroutine
    def get(self):
        self._test()

    @gen.coroutine
    def post(self, *args, **kwargs):
        self._test(*args, **kwargs)
	
    @gen.coroutine
    def _test(self, *args, **kwargs):
        #img_url = 'https://172.23.184.13/sdk_service/rest/videoanalysis/peopleface/image'
        #img_url = 'https://172.23.184.13/sdk_service/rest/videoanalysis/peopleface/image?fileid={}&type={}'
        res, file_name = {}, ""
        try:
            data = json_format(str(self.request.body,'utf-8'))
            if data: 
                cameraid = data["content"]["common-info"]["camera-id"]
                file_name = data["content"]["common-info"]["alarm-pic-name"]
                file_time_c = data["content"]["common-info"]["ctime"]
                image = data["content"]["private-info"]["pic"]["_imageUrl"]
                res['image_url'] = image.replace("amp;", "")
                res['cameraid'] = cameraid
                res['time'] = file_time_c
            else:
                logger.debug("NO DATA")
        except Exception as err:
            logger.debug("{}".format(err))
       	image_url = image.replace("amp;", "")
        image = requests.get(image_url, headers=header, verify=False)
        image_file_b = image.content
        if image_file_b:
            # 获取上传通道和文件上传id
            upload_file_len = str(len(image_file_b))
            upload_url, upload_id = yield self.get_upload_url(file_name, upload_file_len) 
            # 上传图片
            if upload_url and upload_id:
                print("upload_url:{}, upload_id:{}, length:{}, file_name:{},header:{}".format(upload_url, upload_id, upload_file_len, file_name, header_upload))
                m = MultipartEncoder(fields={'action': 'upload', 'uploaded-file-id': upload_id,'begin':'0','length':upload_file_len,'imgInput': (file_name, image_file_b, 'text/plain')})
                header_upload["Content-Type"] = m.content_type
                r = requests.post(url=upload_url, data=m, headers=header_upload, verify=False)
                try:
                    data = json_format(r.text)
                    msg = data["response"]["result"]["errmsg"]
                    code = data["response"]["result"]["code"]
                    if int(code) == 0:
                        uploaded_file_id = data["response"]["upload"]["uploaded-file-id"]
                        casefile_id = self.release(file_time_c, file_name, uploaded_file_id)
                        res["casefile_id"] = casefile_id
                    else:
                        logger.debug("{}".format(msg))
                except Exception as err:
                    logger.debug("{}".format(err))
            else:
                logger.debug("Failed to get upload channel")
        else:
            logger.debug("Download image failed")

        data = json.dumps(res)
        print("result data is :{}".format(data))
        #r = executor.submit(self.send_res, data)
        check_face = Global_configure.check_face
        result= requests.post(url=check_face, data=data, verify=False)  
        print(result.text)
        #self.write(result.text)

    def release(self, file_time, file_name, uploaded_file_id):
        import time
        try:
            timeStamp = float(int(file_time)/1000)
            timeArray = time.localtime(timeStamp)
            otherSryleTime=time.strftime("%Y-%m-%d %H:%M:%S",timeArray)
            time_list = otherSryleTime.split(" ")
            t = time_list[0].replace("-", '') + time_list[1].replace(":", '')
            print("tttttttttttttttttttt",t)
        except Exception as err:
            print(err)
        # 图像信息库发布文件
        casefile_id = ""
        body = release_file_body.format(t, file_name, 0, uploaded_file_id)
        #r = yield tornado_request.post(url=release_file_api, data=body, is_json_result=False, headers=header, validate_cert=False)
        r = requests.post(url=release_file_api, data=body, verify=False, headers=header_rel)
        print(r.text)
        try:
            data = json_format(r.text)
            msg = data["response"]["result"]["errmsg"]
            code = data["response"]["result"]["code"]
            if int(code) == 0:
                casefile_id = data["response"]["result"]["casefileId"]
            else:
                logger.debug("{}".format(msg))
        except Exception as err:
            print(err)
            logger.debug("{}".format(err))

        return casefile_id
        
    
    def send_res(self, data):
        # 推送casefile 信息
        # face = Global_configure.face
        # db_input = Global_configure.db_input
        check_face = Global_configure.check_face
        for url in [check_face]:
            r = yield requests.post(url=url, data=data, verify=False)
            print(r.text)
            return r

    @gen.coroutine
    def download_image(self, url, params):
        # 下载人体图片
        image = None
        try:
            print("url:{}, headers:{}".format(url, header))
            image = yield tornado_request.get(url=url, is_json_result=False, headers=header, params=params)
            print("@@@@@@@@@@@@@@", image.status_code)
        except Exception as err:
            print("=========",err)
            logger.debug("{}".format(err))
        
        return image.content

    @gen.coroutine
    def get_upload_url(self, name, length):
        # protoco 默认为0 https   1为http(效率高)
        upload_url, upload_id = "", ""
        url = get_upload_api + '?name={}&length={}&protocol=1'.format(name, length)
        r = yield tornado_request.get(url=url, is_json_result=False, headers=header)
        print(r.text)
        try:
            data = json_format(r.text)
            msg = data["response"]["result"]["errmsg"]
            code = data["response"]["result"]["code"]
            if int(code) == 0:
                upload_url = data["response"]["result"]["upload"]["url"]
                upload_id = data["response"]["result"]["upload"]["uploaded-file-id"]
            else:
                logger.debug("{}".format(msg))
        except Exception as err:
            logger.debug("{}".format(err))

        return upload_url, upload_id

     

class Application(web.Application):
    def __init__(self):
        settings = dict(
            debug=True,
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        handlers = [
            (r"/test/", CallBackHandler),
            (r"/(.*)", web.StaticFileHandler, {"path": settings['static_path']}),
        ]

        web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    port = 9999
    Application().listen(port)
    print("start at : http://127.0.0.1:{}".format(port))
    tornado.ioloop.IOLoop.current().start()
