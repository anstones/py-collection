#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pika

# ########################## 消费者 ##########################
# 用户名和密码（guest为默认用户，guest默认密码，此账户是不能进行远程连接的账户，需要新建账户(如：test)并授权远程连接）
credentials = pika.PlainCredentials('test', 'test')
# 连接到rabbitmq服务器
# /test1 表示rabbitmq 虚拟主机，还有默认的/，可以自主新建

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.160.128',5672,'/test1',credentials))
channel = connection.channel()

# 声明消息队列，消息将在这个队列中进行传递。如果队列不存在，则创建
channel.queue_declare(queue='wzg')


# 定义一个回调函数来处理，这边的回调函数就是将信息打印出来。
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

# 告诉rabbitmq使用callback来接收信息
channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)
 # no_ack=True表示在回调函数中不需要发送确认标识

print(' [*] Waiting for messages. To exit press CTRL+C')

# 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理。按ctrl+c退出。
channel.start_consuming()