#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import time
import grpc
import json
import traceback
import hashlib

from .rabbitmq_client import RabbitmqClient

RmqHost = "192.168.128.133"
RmqPort = 5672
RmqVHost = "oeasy_vhost_prod"
RmqUser = "oeasy"
RmqPassword = "oeasy"
ConsumeQueueName = "ConsumeQueueName"

exchanges_list = [("facecenter_worker_exchange", "face_center_1", "face_center_1"), 
                    ("facecenter_worker_exchange", "face_center_2", "face_center_2"), 
                    ("facecenter_worker_exchange", "face_center_3", "face_center_3"),
                    ("facecenter_worker_exchange", "face_center_4", "face_center_4")]

class DispatchCenter(object):
    def __init__(self):
        self.exchanges = list(set(exchanges_list))
        self.index = 0
        self.rmq_client = RabbitmqClient(RmqHost, RmqPort, RmqVHost, RmqUser, RmqPassword)
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
                print("begin to publish msg to exchange {} routing_key {}, msg : {}".format(exchange, routing_key, str(msg)))
                self.rmq_client.channel.basic_publish(exchange, routing_key, msg)
                print("publish msg done, msg {}".format(str(msg)))
                break
            except Exception as e:
                print(traceback.format_exc())
                print("publish msg error, msg {}".format(msg))

    def rmq_callback(self, ch, method, properties, body):
        try:
            print("get MQ message: " + body)
            start_time = time.time()
            self.handler_msg(json.loads(body))
            print("MQ message process done, cost time: %s", time.time() - start_time)
        except Exception as e:
            print(traceback.format_exc())
            print("MQ message exception")
            time.sleep(5)
