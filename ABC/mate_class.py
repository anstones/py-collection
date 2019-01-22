#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import itertools 
import collections

def upper_attr(future_class_name, future_class_parents, future_class_attr):
    '''返回一个类对象，将属性都转为大写形式'''
    #选择所有不以'__'开头的属性
    attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
    # 将它们转为大写形式
    uppercase_attr = dict((name.upper(), value) for name, value in attrs)
    #通过'type'来做类对象的创建
    return type(future_class_name, future_class_parents, uppercase_attr)#返回一个类

class Foo(object):
    __metaclass__ = upper_attr
    bar = 'bip' 


# list 去重
ids = [1,4,3,3,4,2,3,4,5,6,1]
news_ids = []
for id in ids:
    if id not in news_ids:
        news_ids.append(id)
print(news_ids)


# list 排序去重
ids = [1,3,3,2,5,6,1]
ids.sort()
it = itertools.groupby(ids)  # 迭代器中相邻的重复元素挑出来放在一起(需要对列表先排序)
for k, g in it:
    print (k)


# 字典key 排序
x={2:1,3:4,4:2,1:5,5:3}
import operator
# sorted_x=sorted(x.items(),key=operator.itemgetter(0))
sorted_x=sorted(x.items(),key=lambda x:x[0])
print(x)
print (sorted_x)
print (dict(sorted_x))



#字典values 排序
x={2:1,3:4,4:2,1:5,5:3}
import operator
# sorted_x=sorted(x.items(),key=operator.itemgetter(1)) 
sorted_x=sorted(x.items(),key=lambda x:x[1])
print(x)
print (sorted_x)
print (dict(sorted_x))

