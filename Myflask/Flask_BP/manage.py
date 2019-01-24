#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask_script import Manager

from APP import create_app
from APP.Index import index
from APP.Admin import admin
from libs.logger import logger

app = create_app()  # 创建app
app.register_blueprint(index, url_prefix='/index')  
app.register_blueprint(admin, url_prefix='/admin')  
# 第一个参数是app.__init__.py下实例化的蓝图对象，
# 第二个参数为url访问时的中间值如：127.0.0.1:5000/admin/; 127.0.0.1:5000/index

manager = Manager(app)  # 通过app创建manager对象

if __name__ == '__main__':
    logger.debug('flask server start')
    logger.info('=================')
    manager.run()
