#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
进度条
"""

import sys,time
for a in range(101):
    #print a
    b = 100 -a
    #print b
    #sys.stdout.write(("\r[%s%s]%0.2f%%" %("#"*a,b*"",float(a))))
    sys.stdout.write(("\r[%s%s]%0.2f%%"%("#"*a,b*" ",float(a))))
    sys.stdout.flush()
    time.sleep(0.1)