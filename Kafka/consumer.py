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