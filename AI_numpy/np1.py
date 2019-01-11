#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import random
import time
import numpy as np

### 1.np.array与list的区别
a = []
for i in range(100000000):
    a.append(random.random())
t1 = time.time()
sum1=sum(a)
t2=time.time()

b=np.array(a)
t4=time.time()
sum3=np.sum(b)
t5=time.time()
print(t2-t1, t5-t4)

### 2. numpy 类型
'''
np.bool	用一个字节存储的布尔类型（True或False）	'b'
np.int8	一个字节大小，-128 至 127	
np.int16	整数，-32768 至 32767	
np.int32	整数，-2 31 至 2**32 -1	
np.int64	整数，-2 63 至 2**63 - 1	
np.uint8	无符号整数，0 至 255	
np.uint16	无符号整数，0 至 65535	
np.uint32	无符号整数，0 至 2**32 - 1
np.uint64	无符号整数，0 至 2**64 - 1
np.object_	python对象
np.string_	字符串
np.unicode_	unicode类型
'''
a = np.array([[1, 2, 3],[4, 5, 6]], dtype=np.float32) # 指定arrry的类型 

### 3. numpy 基本操作

# 生成全为1和0数组
one = np.ones([2,3])
zero = np.zeros([3, 4])

# 从现有的数组当中创建
a = np.array([[1,2,3],[4,5,6]])
a1 = np.array(a)

# 生成等间隔的数组
np.linspace(0, 100, 10)

# 随机数组
np.random.rand() #返回[0.0，1.0)内的一组均匀分布的数。
np.random.randint(1, 10, size=100) #从一个均匀分布中随机采样
np.random.uniform(-1, 1, 100000000) # 生成均匀分布的随机数
np.random.normal(loc=0.0, scale=1.0, size=None) # 0-1 正态分布
7
stock_change = np.random.normal(0, 1, (8, 10))
stock_change  # 创建符合正态分布的8只股票10天的涨跌幅数据

# 形状修改
stock_change.reshape([10, 8]) # 只是将形状进行了修改，但并没有将行列进行转换
stock_change.reshape([-1,20])  # 数组的形状被修改为: (4, 20), -1: 表示通过待计算

# 类型修改
stock_change.astype(type)

stock_change.tostring()
stock_change.tobytes()

# 去重
np.unique(stock_change)

### 4. numpy 切片
stock_change[0, 0:3]
# 逻辑判断--》赋值
stock_change[stock_change > 0.5] = 1

np.all(stock_change[0:2, 0:5] > 0)
np.any(stock_change[0:2, 0:5] > 0)

# 矩阵相乘
a = stock_change[0:6, 0:2]
# b = stock_change[0:6, 4:6]
b = stock_change[1:2, 0:2]
np.dot(a,b)
np.matmul(a, b)