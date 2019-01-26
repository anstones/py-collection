#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import re

# compile 将正则表达式编译成pattern对象，后面可以直接调用
a = re.compile('\d')
s = 'a1b2c3'
res = a.findall(s)
print(res)

