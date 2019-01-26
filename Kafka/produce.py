#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json
from kafka import KafkaProducer


def produce():
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    for i in range(2):
        msg_dict = {
            "db_config": {
                "database": "test_1",
                "host": "localhost",
                "user": "root",
                "password": "password"
            },
            "table": "msg",
            "msg": "测试下的第%s条信息" % i
        }
        msg = json.dumps(msg_dict)
        print(msg)
        re = producer.send('test', key=b'test', value=msg.encode("utf-8"))
    producer.close()
    print(re)


def to_str(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value


if __name__ == '__main__':
    produce()