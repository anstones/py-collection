#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
数组写入csv
"""

import csv
import os

csvfile = open('ho.csv', 'a')
writer = csv.writer(csvfile, dialect='excel',lineterminator="\n")
writer.writerow(['1', '2', '3','4','5'])
data = [
   [3,3,2],[4,4,2],[1,1,0],[2,2,2],[1,1,1]
]
writer.writerows(data)

csvfile.close()