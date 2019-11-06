#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import time
import grpc
import json
import traceback
import hashlib

from core.rabbitmq_client import RabbitmqClient
from lib.lconf import Lconf
from lib.logger import logger

Global_lconf = Lconf()


class DispatchCenter(object):
    def __init__(self):
        self.exchanges = list(set(Global_lconf.WorkExchanges))
        self.index = 0
        self.rmq_client = RabbitmqClient(Global_lconf.RmqHost, 
                                            Global_lconf.RmqPort, 
                                            Global_lconf.RmqVHost, 
                                            Global_lconf.RmqUser, 
                                            Global_lconf.RmqPassword
                                            )
        self.rmq_client.start()
        self._initilize_queue()

    def _initilize_queue(self):
        """
        声明交换，绑定队列
        重复调用不影响
        """
        for exchange, routing_key, queue_name in self.exchanges:
            self.rmq_client.channel.exchange_declare(exchange=exchange, exchange_type='direct', passive=False, durable=True, auto_delete=True)
            self.rmq_client.channel.queue_declare(queue=queue_name, durable=True)
            self.rmq_client.channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=routing_key)

    def handler_msg(self, data):
        exchange, routing_key, queue_name = self.exchanges[self.index]
        self.publish_to_rabbitmq(exchange, routing_key, json.dumps(data))
        self.index = (self.index + 1) % len(self.exchanges)
        return True


    def publish_to_rabbitmq(self, exchange, routing_key, msg):
        """
        发布消息到rabbitmq
        """
        for i in range(3):
            try:
                logger.info("begin to publish msg to exchange {} routing_key {}, msg : {}".format(exchange, routing_key, str(msg)))
                self.rmq_client.channel.basic_publish(exchange, routing_key, msg)
                logger.info("publish msg done, msg {}".format(str(msg)))
                break
            except Exception as e:
                logger.error(traceback.format_exc())
                logger.error("publish msg error, msg {}".format(msg))

    def rmq_callback(self, ch, method, properties, body):
        try:
            logger.info("get MQ message: " + body)
            start_time = time.time()
            self.handler_msg(json.loads(body))
            logger.info("MQ message process done, cost time: %s", time.time() - start_time)
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error("MQ message exception")
            time.sleep(5)
