#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pandas as pd
from mpl_finance import candlestick_ochl
import matplotlib.pyplot as plt

### 某个股票的行情数据

stock_day = pd.read_csv("./data/stock_day.csv")
stock_day = stock_day.sort_index()
# 对每日交易数据进行重采样 （频率转换）
stock_day.index

# 1、必须将时间索引类型编程Pandas默认的类型
stock_day.index = pd.to_datetime(stock_day.index)

# 2、进行频率转换日K---周K,首先让所有指标都为最后一天的价格
period_week_data = stock_day.resample('W').last()

# 分别对于开盘、收盘、最高价、最低价进行处理
period_week_data['open'] = stock_day['open'].resample('W').first()
# 处理最高价和最低价
period_week_data['high'] = stock_day['high'].resample('W').max()
# 最低价
period_week_data['low'] = stock_day['low'].resample('W').min()
# 成交量 这一周的每天成交量的和
period_week_data['volume'] = stock_day['volume'].resample('W').sum()
period_week_data.dropna(axis=0)


# 先画日K线
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(20, 8), dpi=80)
# 准备数据， array数组
stock_day['index'] = [i for i in range(stock_day.shape[0])]
day_k = stock_day[['index', 'open', 'close', 'high', 'low']]
candlestick_ochl(axes, day_k.values, width=0.2, colorup='r', colordown='g')
plt.show()


# 周K线图数据显示出来
period_week_data['index'] = [i for i in range(period_week_data.shape[0])]
week_k = period_week_data[['index', 'open', 'close', 'high', 'low']]
candlestick_ochl(axes, week_k.values, width=0.2, colorup='r', colordown='g')
plt.show()



# 拿到股票K线数据
stock_day = pd.read_csv("./data/stock_day.csv")
stock_day = stock_day.sort_index()
stock_day["index"] = [i for i in range(stock_day.shape[0])]
arr = stock_day[['index', 'open', 'close', 'high', 'low']]
values = arr.values[:200]
# 画出K线图
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(20, 8), dpi=80)
candlestick_ochl(axes, values, width=0.2, colorup='r', colordown='g')

plt.show()