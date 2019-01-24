#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import os.path
import logging
import logging.config
from utils.get_path import get_log_dir


__all__ = ["logger"]


def get_log_config(log_level, log_file_name="logger.log"):
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
                'filename': os.path.join(get_log_dir(), log_file_name),
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

    return log_config


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
        self.level = None
        self.filename = None

    def set_logger(self, new_logger):
        self._logger = new_logger

    def set_level(self, level):
        self.level = level

    def set_filename(self, filename):
        self.filename = filename

    def start(self):
        log_config = get_log_config(self.level, self.filename) if self.filename is not None else get_log_config(self.level)
        logging.config.dictConfig(log_config)

        new_logger = logging.getLogger("logger_basic")
        self.set_logger(new_logger)

    def __getattr__(self, item):
        return getattr(self._logger, item)


logger = LoggerWrap()
