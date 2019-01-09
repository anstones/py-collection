#!/usr/bin/env python
# -*- encoding: utf-8 -*-

str = 'afterUid=c9ec39496ce34527b2c61912670030e1, beforeUid=7019_aa651fa9f2334a41933998a5c7b156c4, unitId=7019, cmd=replace_uid'

d = dict([i.split('=') for i in str.split(',')])

print(d)