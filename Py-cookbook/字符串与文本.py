#!/usr/bin/env python
# -*- encoding: utf-8 -*-

s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
the eyes, not around the eyes, don't look around the eyes, \
look into my eyes, you're under."

import textwrap
# 指定列宽
print(textwrap.fill(s, 30))


#十进制  -->   二进制    八进制   十六进制
# 1234        bin(x)   oct(x)    hex(x)

#   二进制               八进制            十六进制         十进制
#   int(bin(x), 2)   int(oct(x),8)    int(hex(x),16)       1234
