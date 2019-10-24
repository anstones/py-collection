#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pika, threading, uuid, time

# 自定义线程类，继承threading.Thread
class MyThread(threading.Thread):
    def __init__(self, func, num):
        super(MyThread, self).__init__()
        self.func = func
        self.num = num
    
    def run(self):
        print(" [x] Requesting increase(%d)" % self.num)
        response = self.func(self.num)
        print(" [.] increase(%d)=%d" % (self.num, response))

class Center():
    def __init__(self):
        self.credentials = pika.PlainCredentials('oeasy', 'oeasy')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.133.128', 5672, '/', self.credentials))
        self.channel = self.connection.channel()

        # 定义接受返回信息的队列
        result = self.channel.queue_declare("", exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
                                    on_message_callback= self.on_response,
                                    queue=self.callback_queue,
                                    auto_ack=True)
        self.response = {}

    # 定义接收到返回消息的处理方法
    def on_response(self, ch, method, props, body):
        self.response[props.correlation_id] = body

    def request(self, n):
        corr_id = str(uuid.uuid4())
        self.response[corr_id] = None

        # 发送计算请求，并设定返回队列和correlation_id
        self.channel.basic_publish(
            exchange='',
            routing_key='compute',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=corr_id,),
            body=str(n))

        #接收返回的数据
        if self.response[corr_id] is None:
            self.connection.process_data_events()
        return int(self.response[corr_id])

center = Center()
#发起5次计算请求
nums= [10,20]
threads = []
for num in nums:
    # threads.append(MyThread(center.request, num))
    threads.append(threading.Thread(target=center.request, args=(num,)))
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
