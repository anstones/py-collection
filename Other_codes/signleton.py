"""
单例模式
"""

# 基于@classmethod
class SingLeton():

    def __init__(self):
        pass

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(SingLeton, '_instance'):
            SingLeton._instance = SingLeton(*args, **kwargs)
        return SingLeton._instance


# 基于__new__
class SingLeton1():
    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(SingLeton, '_instance'):
            SingLeton1._instance = object.__new__(cls, *args, **kwargs)

        return SingLeton1._instance
                
# 基于装饰器
def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton
 
@singleton
class Test(object):
    pass