#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pandas as pd
import talib
import matplotlib.pyplot as plt
import numpy as np
from mpl_finance import candlestick_ochl

# 读取日线的数据
stock_day = pd.read_csv("./data/stock_day.csv")
stock_day = stock_day.sort_index()[:200]
stock_day['index'] = [i for i in range(stock_day.shape[0])]
arr = stock_day[['index', 'open', 'close', 'high', 'low']].values

print(arr)

dif, dea, macd_hist = talib.MACD(stock_day['close'].values, fastperiod=12, slowperiod=26, signalperiod=9)

# 构造画布，里面包含了一个axes
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(20, 8), dpi=100)

# 产生一个x的单维数组
index = [i for i in range(200)]

# 画出dif这根差离值线
plt.plot(index, dif, color='y', label="差离值 DIF")
plt.plot(index, dea, color='b', label="讯号线 DEA")

# 画出MACD柱状图
# 分开正负的柱状图去画出来
# 画第一个bar， macd_hist，如果大于0， 保留当前值，如果小于0，变为0，得出一个red_hist
# 画出第二个bar，macd_hisr，如果小于0， 保留当前值，如果大于0，直接变为0
red_hist = np.where(macd_hist > 0 , macd_hist, 0)
print(red_hist)
green_hist = np.where(macd_hist < 0 , macd_hist, 0)
print(green_hist)
plt.bar(index, red_hist, label="红色MACD值", color='r')
plt.bar(index, green_hist, label="绿色MACD值", color='g')

# 显示一下K线图对比MACD指标图
candlestick_ochl(axes, arr, width=0.2, colorup='r', colordown='g')

plt.legend(loc="best")
plt.savefig('./MACD.png')
plt.show()