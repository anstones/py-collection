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

def dev_format(devices):
    if not isinstance(devices, list):
        devices = [devices]
    tmp = []
    for dev in devices:
        if dev == "":
            continue
        if len(dev) == len("0000000000_001122334455"):
            tmp.append(dev.lower())  # mac地址小写
        else:
            tmp.append(dev)
        if dev.startswith("0000003925"):  # 这两个小区可以互相识别
            tmp.append(dev.replace("0000003925", "0000003929"))
        elif dev.startswith("0000003929"):
            tmp.append(dev.replace("0000003929", "0000003925"))

    return tmp
