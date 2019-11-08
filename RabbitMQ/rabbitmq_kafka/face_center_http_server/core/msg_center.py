#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import grpc
import json
import traceback

# from models import Feature
from rpc import kafka_push_pb2, kafka_push_pb2_grpc
from rpc import ws_push_pb2, ws_push_pb2_grpc
from core.mq_center import MQHandler
from lib.lconf import Lconf
from lib.logger import logger
from lib.utils import *

Global_lconf = Lconf()


class MsgCenter(object):
    retry_add_table = dict()
    retry_replace_table = dict()
    mq_handler = MQHandler()

    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        if Global_lconf.is_push_kafka_or_ws == 1:
            kafka_push_channel = grpc.insecure_channel(Global_lconf.GrpcKafkaPushServer)
            self.kafka_push_stub_ = kafka_push_pb2_grpc.KafkaProduceHandlerStub(kafka_push_channel)

            ws_push_channel = grpc.insecure_channel(Global_lconf.GrpcWsPushServer)
            self.ws_push_stub_ = ws_push_pb2_grpc.WsPushHandlerStub(ws_push_channel)

    def handler_msg(self, data):
        """ 消息处理 """
        cmd = data.get('cmd', '')
        users = data.get('users', '')
        if users == '':
            return common_response(False, 'users(null) is not allowed')

        if not isinstance(users, list):
            users = [users]
        if cmd.endswith('user'):  # 处理人脸录入模块添加和删除用户请求
            feature_id = data.get('feature_id', 0)
            logger.info("cmd: %s, users: %s, feature_id: %s", cmd, users, feature_id)
            print("通过人脸录入莫款添加和删除用户")

        else:  # 处理物业平台授权解除授权请求
            origin_devices = data.get('devices', None)
            self.start_time = data.get("start_time", 0)
            self.end_time = data.get("end_time", 0)
            if not origin_devices:
                return common_response(False, '%s: devices(null) is not allowed' % cmd)

            devices = dev_format(origin_devices)
            if cmd == 'add_device':
                # 添加设备和用户的对应关系，area如果没有会自动生成
                logger.info("add_device {}".format(devices))
                print("添加设备和用户的对应关系，area如果没有会自动生成")
                self.distribute(
                                    {'type': 'add_user',
                                     'data': {d.device: users}
                                     })


            elif cmd == 'del_device':
                # 删除设备和用户的对应关系
                logger.info("del_device {}".format(devices))
                print("删除设备和用户的对应关系")

        return common_response(True, '')

    def update_feature(self, u, feature_id, feature):
        """ 更新特征 """
        print("update feature for user: %s", u)
        self.distribute({'type': 'update_feature',
                            'data': [{'uid': u.uid,
                                        'pic_md5': u.pic_md5,
                                        'feature_id': f.feature_id,
                                        'feature': f.feature
                                        }]
                            })

    def distribute(self, msg):
        """
        分发消息到ws客户端和kafka客户端
        """
        area = "010101"
        if Global_lconf.is_push_kafka_or_ws == 1:
            data = json.dumps({"topic": "feature/{}".format(area), "data": msg})

            try:
                logger.info("begin to push msg to kafka client, area {}".format(area))
                self.kafka_push_stub_.PushToKafka(kafka_push_pb2.KafkaProduceRequest(data=data))
                logger.info("push to kafka client done")
            except Exception as e:
                logger.error(traceback.format_exc())
                logger.error("push_to_kafka error")

            try:
                logger.info("begin to push msg to ws client, area {}".format(area))
                self.ws_push_stub_.PushToWsClient(ws_push_pb2.WsPushRequest(area=area, data=json.dumps(msg)))
                logger.info("push to ws client done, area {}".format(area))
            except Exception as e:
                logger.error(traceback.format_exc())
                logger.error("push to ws client error, area {}".format(area))
        else:
            pass
