#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# 向一个文件中写入数据，但是前提必须是这个文件在文件系统上不存在

# with open('somefile', 'wt') as f:
with open('somefile', 'xt') as f:
    f.write('Hello\n')
