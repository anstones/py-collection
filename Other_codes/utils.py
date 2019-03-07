# coding:utf-8

import os
import sys
import time
import random
from datetime import datetime


def get_script_path():
    real_path = os.path.realpath(sys.argv[0])
    real_file = os.path.split(real_path)
    return real_file[0]


def get_rel_script_path():
    script_path = get_script_path()
    rel_path = os.path.relpath(os.getcwd(), script_path)
    return rel_path


def is_script_path():
    return get_rel_script_path() == "."


def get_log_dir():
    log_dir = os.path.join(get_script_path(), 'log')
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    return os.path.join(get_script_path(), 'log')


def get_config_dir():
    if is_script_path():
        return os.path.join(get_script_path(), "conf")
    else:
        return os.path.join(os.getcwd(), '..', 'conf')


def datetime_toString(dt):
    """
    datetime转成字符串
    :param dt:
    :return:
    """
    return dt.strftime("%Y-%m-%d")


def string_toDatetime(string):
    """
    把字符串转成datetime
    :param string:
    :return:
    """
    return datetime.strptime(string, "%Y-%m-%d %X")


def string_toTimestamp(strTime):
    """
    把字符串转成时间戳形式
    :param strTime:
    :return:
    """
    return time.mktime(string_toDatetime(strTime).timetuple())


def timestamp_toString(stamp):
    """
    把时间戳转成字符串形式
    :param stamp:
    :return:
    """
    return time.strftime("%Y-%m-%d-%H", time.localtime(stamp))


def datetime_toTimestamp(dateTim):
    """
    把datetime类型转外时间戳形式
    :param dateTim:
    :return:
    """
    return time.mktime(dateTim.timetuple())


def generate_timestamp():
    """生成 timestamp
    :return: timestamp string
    """
    return int(time.time())


def generate_nonce():
    """生成 nonce
    :return: nonce string
    """
    return random.randrange(1000000000, 2000000000)


def twins(cls):
    cls.Dict_arg_instance = dict()

    def _warpper(*arg,**kwars):
        topic = kwars.get("topic","")
        if not topic:
            return cls()
        if not topic in cls.Dict_arg_instance:
            cls.Dict_arg_instance[topic] = cls(*arg,**kwars)
        return cls.Dict_arg_instance[topic]
    return _warpper

def single_ton(cls):
    ins = dict()
    def _warpper(*arg,**kwars):
        if not cls in ins:
            obj = cls(*arg,**kwars)
            ins[cls] = obj
        return ins[cls]
    return _warpper

def short_str(data, max_len=500):
    if len(data)>max_len:
        return data[:500]+"...."
    return data