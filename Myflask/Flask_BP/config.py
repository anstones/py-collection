#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os

BASE_DIR = os.getcwd()  # 项目的绝对路径 

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')  # 模板文件的路径

STATICFILES_DIR = os.path.join(BASE_DIR, 'static')  # 静态文件的路径

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@192.168.160.128:3306/mine'  # 数据库URI

SQLALCHEMY_TRACK_MODIFICATIONS = True  # 查询跟踪，不太需要，False，不占用额外的内存