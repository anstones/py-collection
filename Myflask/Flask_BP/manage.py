#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask_script import Manager

from APP import create_app
from APP.Index import index
# from APP.Admin import admin

app = create_app()  # 创建app
app.register_blueprint(index, url_prefix='/indexs')  # 注册蓝图
# app.register_blueprint(admin, url_prefix='/admin')  # 注册蓝图

manager = Manager(app)  # 通过app创建manager对象

if __name__ == '__mian__':
    manager.run()  # 运行服务器
