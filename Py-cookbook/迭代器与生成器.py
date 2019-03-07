#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# 迭代一个序列的同时跟踪正在被处理的元素索引
my_list = ['a', 'b', 'c']
for idx, val in enumerate(my_list, 1):
    print(idx, val)


# 迭代遍历一个集合中元素的所有可能的排列或组合
from itertools import permutations, combinations
items = ['a', 'b', 'c']
for p in permutations(items):
    print(p)

for c in combinations(items, 3):
    print(c)

# 同时迭代多个序列，每次分别从一个序列中取一个元素。
xpts = [1, 5, 4, 2, 10, 7]
ypts = [101, 78, 37, 15, 62, 99]
for x, y in zip(xpts, ypts):
    print(x,y)

# 同时迭代多个序列,序列长度不同时，fillvalue 填充None
from itertools import zip_longest
a = [1, 2, 3]
b = ['w', 'x', 'y', 'z']
for i in zip_longest(a, b, fillvalue=0):
    print(i)

# 迭代不同序列的所有元素
from itertools import chain
a = [1, 2, 3, 4]
b = ['x', 'y', 'z']
for x in chain(a, b):
    print(x)

# 将一个多层嵌套的序列展开成一个单层列表
from collections import Iterable

def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x

items = [1, 2, [3, 4, [5, 6], 7], 8]
for x in flatten(items):
    print(x)

# 有一系列排序序列，想将它们合并后得到一个排序序列并在上面迭代遍历
import heapq
a = [1, 4, 7, 10]
b = [2, 5, 6, 11]
for c in heapq.merge(a, b):
    print(c)