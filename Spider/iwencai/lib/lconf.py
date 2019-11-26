#coding:utf8
from lib.getconf import getConfig
from lib.utils import *


@singleton
class Lconf(object):
    """docstring for Lconf"""
    def __init__(self):
        self.account          = getConfig("Login", "account")
        self.passdord         = getConfig("Login", "passdord")
        self.login_url        = getConfig("Login", "url")

        self.url_first        = getConfig("GetPage", "url_1")
        self.url_second       = getConfig("GetPage", "url_2")

        self.code_count       = getConfig("Count", "code_count")

        self.token            = getConfig("Token","token")
        self.day_list         = getConfig("Day", "day")

        self.sleep_time       = getConfig("Sleep", "sleep_time")
