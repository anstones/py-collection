#coding:utf8
from getconf import getConfig

def singleton(cls):
    instance = dict()

    def _wrapper(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return _wrapper

@singleton
class Lconf(object):
    """docstring for Lconf"""
    def __init__(self):
        self.account          = getConfig("Login", "account")
        self.passdord         = getConfig("Login", "passdord")
        self.login_url        = getConfig("Login", "url")

        self.url              = getConfig("GetPage", "url")
        self.url_ajax         = getConfig("GetPage", "url_ajax")

        self.code_count       = getConfig("Count", "code_count")

        self.token            = getConfig("Token","token")
        self.day_list         = getConfig("Day", "day")

        self.sleep_time       = getConfig("Sleep", "sleep_time")

        self.params           = int(getConfig("OpenDay", "params"))
