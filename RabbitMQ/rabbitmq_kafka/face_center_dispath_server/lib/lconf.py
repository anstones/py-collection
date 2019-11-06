#coding:utf8
from .getconf import getConfig
from .utils import *

@singleton
class Lconf(object):
    """docstring for Lconf"""
    def __init__(self):

        self.LogLevel            = getConfig("Log", "Level")

        self.RmqHost             = getConfig("RabbitMqInfo", "Host")
        self.RmqPort             = int(getConfig("RabbitMqInfo", "Port"))
        self.RmqVHost            = getConfig("RabbitMqInfo", "VHost")
        self.RmqUser             = getConfig("RabbitMqInfo", "User")
        self.RmqPassword         = getConfig("RabbitMqInfo", "Password")

        self.PublishExchange     = getConfig("ExchangeInfo", "PublishExchange")
        self.PublishRoutingKey   = getConfig("ExchangeInfo", "PublishRoutingKey")
        self.WorkExchanges       = eval(getConfig("ExchangeInfo", "WorkExchanges"))

        self.ConsumeQueueName    = getConfig("Server", "ConsumeQueueName")
