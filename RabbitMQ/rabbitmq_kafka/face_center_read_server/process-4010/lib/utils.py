import os
import sys
import json

def singleton(cls):
    instance = dict()

    def _wrapper(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return _wrapper

def get_script_path():
    real_path = os.path.realpath(sys.argv[0])
    real_file = os.path.split(real_path)
    return real_file[0]

def get_log_dir():
    return os.path.join(get_script_path(), 'log')

def common_response(result, info):
    json_rst = {'result': result, 'info': info}
    return json.dumps(json_rst)
