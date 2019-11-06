#coding:utf8
from .getconf import getConfig
from .utils import *

@singleton
class Lconf(object):
    """docstring for Lconf"""
    def __init__(self):
        self.ServerPort          = int(getConfig("SevInfo", "Port"))
        self.ServerType          = getConfig("SevInfo", "Type")

        self.LogLevel            = getConfig("Log", "Level")

        self.RmqHost             = getConfig("RabbitMqInfo", "Host")
        self.RmqPort             = int(getConfig("RabbitMqInfo", "Port"))
        self.RmqVHost            = getConfig("RabbitMqInfo", "VHost")
        self.RmqUser             = getConfig("RabbitMqInfo", "User")
        self.RmqPassword         = getConfig("RabbitMqInfo", "Password")

        self.is_push_kafka_or_ws = int(getConfig("ThirdServer", "is_push_kafka_or_ws"))
        self.GrpcKafkaPushServer = getConfig("ThirdServer", "GrpcKafkaPush")
        self.GrpcWsPushServer    = getConfig("ThirdServer", "GrpcWsPush")

        self.PublishExchange     = getConfig("ExchangeInfo", "PublishExchange")
        self.PublishRoutingKey   = getConfig("ExchangeInfo", "PublishRoutingKey")

