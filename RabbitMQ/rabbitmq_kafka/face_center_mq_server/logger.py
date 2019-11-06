# coding: utf-8

from __future__ import print_function
import os
import sys
import os.path
from tornado.options import define, options
import logging
import logging.config
from lib.utils import get_log_dir

from .lconf import Lconf
Global_lconf = Lconf()

log_level = Global_lconf.LogLevel
log_name = "logger.log" if len(sys.argv) <= 1 else sys.argv[1] + "_logger.log"

__all__ = ["logger"]

log_config = {
    'version': 1,
    'formatters': {
        'format1': {
            'class': 'logging.Formatter',
            'format': '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': log_level,
            'formatter': 'format1',
            'filters': []
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'format1',
            'level': log_level,
            'filename': os.path.join(get_log_dir(), log_name),
            'maxBytes': 50 * 1024 * 1024,
            'backupCount': 10
        }
    },
    'root': {
        'handlers': ['console'],
        'filters': [],
        'level': 'NOTSET'
    },
    'loggers': {
        'logger_basic': {
            'handlers': ['file'],
            'filters': [],
            'level': log_level,
            'propagate': True
        }
    }
}
logging.config.dictConfig(log_config)


class SimpleLogger(object):
    @classmethod
    def debug(cls, msg, *args):
        pass

    @classmethod
    def info(cls, msg, *args):
        print(msg, *args)

    @classmethod
    def warning(cls, msg, *args):
        print(msg, *args)

    @classmethod
    def error(cls, msg, *args):
        print(msg, *args)


class LoggerWrap(object):
    def __init__(self, logger_cls=SimpleLogger):
        self._logger = logger_cls()

    def set_logger(self, new_logger):
        self._logger = new_logger

    def __getattr__(self, item):
        return getattr(self._logger, item)


logger = LoggerWrap()


def change_logger():
    global logger
    if options.use_logging:
        new_logger = logging.getLogger("logger_basic")
        logger.set_logger(new_logger)


define("use_logging", type=bool, default=True, help="Use logging module or not")
options.add_parse_callback(change_logger)
