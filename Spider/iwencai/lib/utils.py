from lib.lconf import Lconf

Global_lconf = Lconf()

def singleton(cls):
    instance = dict()

    def _wrapper(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return _wrapper


def is_next(total):
    if total > int(Global_lconf.code_count):
        p = total // int(Global_lconf.code_count) + 1
        return p
    else:
        return None

def open_file(parms):
    f = open('../data/{}.csv'.format(parms), 'w', encoding='utf-8-sig', newline="")
    return f

def up_file(parms):
    f = open('../data/{}.csv'.format(parms), 'a', encoding='utf-8-sig', newline="")
    return f
