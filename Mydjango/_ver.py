
# 获取当前python解释器版本
import sys
import os

ver = sys.version_info
print(ver)

env = os.getenv('HOME')
print(env)
