#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys

def get_script_path():
    real_path = os.path.abspath(os.path.join(os.getcwd(), "../"))
    return real_path


def get_log_dir():
    log_dir = os.path.join(get_script_path(), 'logs')
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    return os.path.join(get_script_path(), 'logs')
