#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import time
import grpc
import json
import traceback
import hashlib

from lib.rabbitmq_client import RabbitmqClient
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
        # exchange, routing_key, queue_name = self.exchanges[self.index]
        # self.publish_to_rabbitmq(exchange, routing_key, json.dumps(data))
        # self.index = (self.index + 1) % len(self.exchanges)
        # return True
        devices = data.get('devices', None)
        if not devices:
            logger.error("devices is null, {}".format(data))
            return False
        if not isinstance(devices, list):
            devices = [devices]

        for dev in devices:
            index = self.get_hash_index(dev)
            exchange, routing_key, _ = self.exchanges[index]
            msg = {"send":data, "device":dev}
            self.publish_to_rabbitmq(exchange, routing_key, json.dumps(msg))    


    def get_hash_index(self, device):
        """ 将设备号device哈希加密然后取模计算，达到同一个device请求送达到同一个队列 """
        md5_inst = hashlib.md5()
        md5_inst.update(device)
        hash_ret = md5_inst.hexdigest()
        value = int(hash_ret[:4], 16)  # 取前四位
        index = value % len(self.exchanges)  # 直接取模
        if index >= len(self.exchanges):
            index = len(self.exchanges) - 1
        return index

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
