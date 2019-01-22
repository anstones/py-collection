#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
装饰器装饰类中的方法时，可以用args实现类“self”的传递
'''

def recontent(func):
    def inner(*args, **kwargs):
        self = args[0]
        print(self.name)
        for arg in args:
            print(arg)
        m = func(*args, **kwargs)
        print(m)
    return inner


class foo():
    def __init__(self,name):
        self.name = name

    @recontent
    def add(self, a, b):
        m = a+b
        return m

fo = foo('fuck')
fo.add(5,8)
