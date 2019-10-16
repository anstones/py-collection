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
                