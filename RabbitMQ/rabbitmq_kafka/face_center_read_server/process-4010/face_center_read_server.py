#!/usr/bin/env python
# coding:utf-8

import tornado
from tornado import httpserver
from tornado import gen, web
from tornado.ioloop import IOLoop
from datetime import datetime
import traceback
import json
import time
import os
import sys

from lib.logger import logger
from lib.lconf import Lconf
from lib.utils import common_response
from core.database import init_db, db_session
from core.models import User
from core.msg_query import query_estate_limit, query_user, query_area_code, query_user_tag, query_ttl_info
from core.feature import Feature

Global_lconf = Lconf()
feature_inst_ = Feature()


class QueryEstateHandler(web.RequestHandler):
    def initialize(self):
        init_db()

    def on_finish(self):
        db_session.remove()

    @gen.coroutine
    def get(self, id):
        result = query_estate_limit(id)
        self.write(result)


class QueryUserHandler(web.RequestHandler):
    def initialize(self):
        init_db()

    def on_finish(self):
        db_session.remove()

    @gen.coroutine
    def get(self, id):
        result = query_user(id)
        self.write(result)


class QueryAreaCodeHandler(web.RequestHandler):
    def initialize(self):
        init_db()

    def on_finish(self):
        db_session.remove()

    @gen.coroutine
    def get(self, id):
        result = query_area_code(id)
        self.write(result)


class FacePictureHandler(web.RequestHandler):
    def on_finish(self):
        db_session.remove()

    def get(self):
        uid = self.get_argument("uid", "")
        if not uid:
            res = common_response(False, "parameter error")
            self.write(res)
            return
        user = User.query.filter_by(uid=uid).first()
        if not user:
            res = common_response(False, "no such a user")
            self.write(res)
            return
        data = dict()
        for i, md5 in enumerate(user.pic_md5):
            data[i] = md5
        res = common_response(True, data)
        self.write(res)
        return


class FeatureHandler(web.RequestHandler):
    """
    ?area=estate&device=devices&timestamp=timestamp&add_del_done=0&mac_address=mac_address
    ?area=0000000000&device=0000000000_0000,0000000002_0011&timestamp=-1&add_del_done=0&mac_address=00:E0:70:54:29:4A
    """

    def initialize(self):
        self._handler = feature_inst_
        init_db()

    def on_finish(self):
        db_session.remove()

    @gen.coroutine
    def get(self):
        result = {}
        area = self.get_argument("area", "")
        device = self.get_argument("device", '')
        timestamp = self.get_argument("timestamp", "")
        mac_address = self.get_argument("mac_address", "")
        add_del_done = int(self.get_argument("add_del_done", 0))
        limit = int(self.get_argument("limit", 50))
        ttl = int(self.get_argument("ttl", 0))

        device_request = device.split(',') if device else ""
        # print("====================", area, device, timestamp, mac_address, add_del_done)
        result = self._handler.get_feature(area, device_request, timestamp, mac_address, add_del_done, limit, ttl)
        self.write(result)


class UserTagHandler(web.RequestHandler):

    def get(self):
        result = {}
        area = self.get_argument("area", "")
        if not area:
            self.write(result)
            logger.debug("area is null")
            return
        try:
            timestamp = int(self.get_argument("timestamp", 0))
            limit = int(self.get_argument("limit", 50))
        except ValueError as e:
            logger.error("parameter error %s", e)
        else:
            result = query_user_tag(area, timestamp, limit)
        finally:
            self.write(result)


class TTLInfoHandler(web.RequestHandler):
    """device = None, page_no = 1, page_size = 10"""

    def get(self):
        area = self.get_argument("area")
        device = self.get_argument("device")
        page_no = self.get_argument("page_no")
        page_size = self.get_argument("page_size")


class TestHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.write("{} start ok".format(Global_lconf.ServerPort))

    @gen.coroutine
    def post(self):
        self.write("{} start ok".format(Global_lconf.ServerPort))


class Application(web.Application):
    def __init__(self):
        settings = dict(
            debug=True,
            static_path=os.path.join(os.path.dirname(__file__), "static")
        )

        handlers = [
            (r"/yihao01-sync-tolocal-v2/query_estate_limit/(.*)", QueryEstateHandler,),
            (r"/yihao01-sync-tolocal-v2/query_user/(.*)", QueryUserHandler,),
            (r"/yihao01-sync-tolocal-v2/query_area_code/(.*)", QueryAreaCodeHandler,),
            (r"/yihao01-sync-tolocal-v2/get_feature", FeatureHandler),
            (r"/yihao01-sync-tolocal-v2/get_tag_info", UserTagHandler),
            (r"/yihao01-sync-tolocal-v2/get_pictures", FacePictureHandler),
            (r"/yihao01-sync-tolocal-v2/test", TestHandler),
            (r"/(.*)", web.StaticFileHandler, {"path": settings['static_path']}),
        ]

        web.Application.__init__(self, handlers, **settings)


def main():
    port = int(sys.argv[1])
    tornado.options.parse_command_line()
    Application().listen(port)
    n_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    logger.info("%s Server start port:%s at the time:%s %s", "*" * 20, Global_lconf.ServerPort, n_time, "*" * 20)
    IOLoop.current().start()


if __name__ == "__main__":
    main()
