#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os


# 向一个文件中写入数据，但是前提必须是这个文件在文件系统上不存在

# with open('somefile', 'wt') as f:
# with open('somefile', 'xt') as f:
#     f.write('Hello\n')

# 获取某个目录中的文件列表：
# names = os.listdir('somedir')



from collections import namedtuple
import csv

with open('data.csv') as f:
    f_csv = csv.reader(f)
    headings = next(f_csv)
    Row = namedtuple('Row', headings)
    for r in f_csv:
        row = Row(*r)
        print(row.Symbol)

with open('data.csv') as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
        print(row["Symbol"])
