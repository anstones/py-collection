#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json

from kafka import KafkaConsumer


def consumer():
    com = KafkaConsumer('test', bootstrap_servers=['192.168.160.128:9092'])
    for msg in com:
        value=json.loads(msg.value)
        rec = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, value)
        print(rec)


if __name__ == "__main__":
    consumer()

# 用第三方库 pykafka 连接kafka
from pykafka import KafkaClient
 
client = KafkaClient(hosts='192.168.160.128:9092')
topic = client.topics['wk']  # 连接名为 wk 的topic
 
consumer = topic.get_simple_consumer()
for j in range(100):
    message = consumer.consume()
    if message is None:
        break
    else:
        print('vauel:'+message.value)
        print('offset:'+str(message.offset))
 
consumer.commit_offsets()
consumer.stop()
