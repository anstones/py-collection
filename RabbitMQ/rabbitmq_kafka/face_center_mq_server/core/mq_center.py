#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import time
import json
import traceback

from .lconf import Lconf
from .logger import logger
from .rabbitmq_client import RabbitmqClient

global_lconf = Lconf()

class MQHandler(object):
    def __init__(self):
        super(MQHandler, self).__init__()
        self.rmq_client = RabbitmqClient(global_lconf.RmqHost, 
                                            global_lconf.RmqPort, 
                                            global_lconf.RmqVHost, 
                                            global_lconf.RmqUser, 
                                            global_lconf.RmqPassword
                                            )
        self.rmq_client.start()

    def publish_to_rabbitmq(self, exchange, routing_key, msg):
        for i in range(3):
            try:
                logger.info("begin to publish msg to rabbitmq exchange: %s, routing_key: %s, mes: %s", exchange,
                            routing_key, str(msg))
                self.rmq_client.channel.basic_publish(exchange, routing_key, msg)
                logger.info("publish msg done, msg: %s", str(msg))
                break
            except Exception as e:
                # print(traceback.format_exc())
                logger.error("publish msg error, msg: %s", str(msg))

    def mq_callback(self, ch, method, properties, body):
        try:
            logger.info("get MQ message: " + str(body))
            start_time = time.time()

            from .msg_center import MsgCenter
            msg_center_inst = MsgCenter()
            msg_center_inst.handler_msg(json.loads(body))
            logger.info("MQ message process done, cost time: %s", time.time() - start_time)
        except Exception as e:
            # 出错，消息返回给rabbitmq
            self.publish_to_rabbitmq(global_lconf.PublishExchange, global_lconf.PublishRoutingKey, body)
            logger.error("get some exceptions during deal mq msg, have return the msg to rabbitmq")
            logger.error(traceback.format_exc())
