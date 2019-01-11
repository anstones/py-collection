#!/usr/bin/env python
# -*- encoding: utf-8 -*
import pandas as pd
import numpy as np

stock_change = np.random.randint(1, 5, (10, 5))

# 使用Pandas中的数据结构
stock_change = pd.DataFrame(stock_change)

# 构造行索引序列
stock_code = ['股票' + str(i) for i in range(stock_change.shape[0])]

# 添加行索引
data = pd.DataFrame(stock_change, index=stock_code)

# 生成一个时间的序列，略过周末非交易日
date = pd.date_range('2017-01-01', periods=stock_change.shape[1], freq='B')

# index代表行索引，columns代表列索引
data = pd.DataFrame(stock_change, index=stock_code, columns=date)

print(stock_change)
print(data)