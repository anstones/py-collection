#!/usr/bin/env python
# -*- encoding: utf-8 -*-

a = [1,2,7]
b = [3,4,5]

# 合并两个有序列表
def merge_sortedlist(a,b):
    c = []
    while a and b:
        if a[0] >= b[0]:
            c.append(b.pop(0))
        else:
            c.append(a.pop(0))
    while a:
        c.append(a.pop(0))
    while b:
        c.append(b.pop(0))
    return c
print (merge_sortedlist(a,b))
