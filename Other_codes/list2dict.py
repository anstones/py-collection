#!/usr/bin/env python
# -*- encoding: utf-8 -*-

ks = ['中国人', '水电费', '观后感', '维吾尔', '观后感aaa', '维吾尔bbb', '中国人aa', '水电费bb']
fz = ['中国', '水电费', '观后感', '维吾尔']

d = {k: [v for v in ks if k in v] for k in fz}
print(d)