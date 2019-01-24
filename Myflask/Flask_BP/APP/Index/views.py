#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from APP.Index import index  # 获取蓝图

from APP.Index.models import *  # 获取数据库模型对象和SQLAlchemy对象db，注意不可使用App模块中的db

@index.route('/')  # 设置路由
def indexs():  # 执行的方法
    return 'This Page Is Index'
