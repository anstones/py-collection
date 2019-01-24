#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy()  # 初始化SQLAlchemy

def create_app():
    """ 创建app的方法 """
    app = Flask(__name__)  # 生成Flask对象
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI  # 配置app的URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app=app)  # SQLAlchemy初始化App
    # 在这还可以设置好配置后， 初始化其他的模块

    return app  # 返回Flask对象app 
