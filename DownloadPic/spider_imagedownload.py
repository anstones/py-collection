#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import scrapy
from scrapy.utils.project import get_project_settings, data_path, project_data_dir
from scrapy.pipelines.images import ImagesPipeline


class DownloadsPipeline(ImagesPipeline):
    # 获取setting文件内图片文件夹的路径
    IMAGES_STORE = get_project_settings().get('IMAGES_STORE')

    # 将需要下载的图片提交请求，不需要指定callback
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['pic_url'])

    def item_completed(self, results, item, info):
        # 原存储路径 status: true or false 
        images = [data['path'] for status, data in results if status]
        # 拼接就图片名
        old_name = self.IMAGES_STORE + os.sep + images[0]
        # 创建新文件名
        # name = "{}_{}_{}.jpg".format(item['name'], item["uid"], item["vid"])
        name = "{}.jpg".format(item['name'])
        new_name = self.IMAGES_STORE + os.sep + images[0].split(os.sep)[0] + os.sep + name
        # 重命名
        os.rename(old_name, new_name)

        item['image_path'] = new_name

        return item