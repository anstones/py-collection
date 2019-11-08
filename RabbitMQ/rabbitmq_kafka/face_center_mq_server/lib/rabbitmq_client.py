#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import threading
import time

from .lconf import Lconf

global_lconf = Lconf()

class RabbitmqClient(threading.Thread):
    def __init__(self, host, port, vhost, user, password, heartbeat_interval=None, blocked_connection_timeout=None):
        super(RabbitmqClient, self).__init__()
        self.host = host
        self.port = port
        self.vhost = vhost
        self.user = user
        self.password = password
        self.heartbeat_interval = heartbeat_interval
        self.blocked_connection_timeout = blocked_connection_timeout
        self.connect()

    def connect(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(self.host,
                                                                       self.port,
                                                                       self.vhost,
                                                                       heartbeat=self.heartbeat_interval,
                                                                       blocked_connection_timeout=self.blocked_connection_timeout,
                                                                       credentials=pika.PlainCredentials(self.user, self.password)))
        self._channel = self._connection.channel()

    def run(self):
        while True:
            if self._connection.is_open:
                self._connection.process_data_events()
            else:
                self.connect()
            time.sleep(5)

    @property
    def connection(self):
        # 通道处于关闭状态，连接正常，重新获取通道
        if self._connection.is_open:
            return self._connection

        # 连接断开，重新建立连接获取通道
        self.connect()
        return self._connection

    @property
    def channel(self):
        # 通道处于打开状态，直接返回
        if self._channel.is_open:
            return self._channel
 
        self._channel = self.connection.channel()
        return self._channel
