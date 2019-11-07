# !/usr/bin/env python
# coding: utf-8

import tornado
from tornado import gen, web
from tornado.ioloop import IOLoop
import traceback
import json
import time
import sys
import os

from core.msg_center import MsgCenter
from core.rabbitmq_client import RabbitmqClient
from core.mq_center import MQHandler
from lib.lconf import Lconf
from lib.logger import logger
from lib.utils import common_response

Global_lconf = Lconf()


msg_center_inst_ = MsgCenter()
mq_handler_inst_ = MQHandler(Global_lconf.RmqHost, 
                                Global_lconf.RmqPort, 
                                Global_lconf.RmqVHost, 
                                Global_lconf.RmqUser, 
                                Global_lconf.RmqPassword
                                )


class CenterMsgHandler(web.RequestHandler):
    """add user, delete user, add device, del device"""

    def initialize(self):
        self._handler = msg_center_inst_
        logger.error(traceback.format_exc())


    @gen.coroutine
    def post(self):
        res = common_response(False, "unkown error")
        try:
            data = json.loads(self.request.body)
            res = self._handler.handler_msg(data)
        except:
            logger.error(traceback.format_exc())
            logger.error('rollback database')
        self.write(res)


class Application(web.Application):

    def __init__(self):
        settings = dict(
            debug=True,
            static_path=os.path.join(os.path.dirname(__file__), "static")
        )

        handlers = [
            (r"/yihao01-sync-tolocal/face_center", CenterMsgHandler,),
            (r"/(.*)", web.StaticFileHandler, {"path": settings['static_path']}),
        ]

        web.Application.__init__(self, handlers, **settings)


def start_rmq_listen():
    queue = sys.argv[1]
    n_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    logger.info("%s Rabbitmq consumer start at the time: %s, the Queue is %s, %s", "*" * 10, n_time, queue, "*" * 10)

    mq_conn = RabbitmqClient(Global_lconf.RmqHost, 
                                Global_lconf.RmqPort, 
                                Global_lconf.RmqVHost, 
                                Global_lconf.RmqUser, 
                                Global_lconf.RmqPassword
                                )
    mq_conn.start()

    while True:
        try:

            mq_conn.channel.queue_declare(queue=queue, durable=True)
            while True:
                method, properties, body = mq_conn.channel.basic_get(queue=queue, no_ack=True)
                if all((method, properties, body)):
                    mq_handler_inst_.mq_callback(mq_conn.channel, method, properties, body)
                else:
                    time.sleep(5)
            # mq_conn.channel.basic_qos(prefetch_count=1)
            # mq_conn.channel.basic_consume(mq_handler_inst_.mq_callback, queue, no_ack=False)
            # logger.info("%s start consuming MQ messgae %s", "*" * 20, "*" * 20)
            # mq_conn.channel.start_consuming()
        except Exception as e:
            # logger.error(traceback.format_exc())
            logger.error("rabbitmq error: %s", str(e))
            time.sleep(5)



def start_http_listen():
    Application().listen(Global_lconf.ServerPort)
    n_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    logger.info("%s Http Server start port: %s at the time: %s %s", "*" * 20, Global_lconf.ServerPort, n_time, "*" * 20)
    IOLoop.current().start()


def main():
    # init_db() # 建表
    tornado.options.parse_command_line() # 用于转换命令行的参数

    if "http_server" == Global_lconf.ServerType:
        start_http_listen()
    else:
        if not len(sys.argv) >= 2:
            logger.info("need to piont the queue of rqbbitmq")
        else:
            start_rmq_listen()


if __name__ == "__main__":
    main()
