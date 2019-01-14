#!/usr/bin/env python
# -*- encoding: utf-8 -*
import pandas as pd
import numpy as np

stock_change = np.random.randint(1, 5, (10, 5))
####################################################################################
# 使用Pandas中的数据结构
stock_change = pd.DataFrame(stock_change)

# 构造行索引序列
stock_code = ['股票' + str(i) for i in range(stock_change.shape[0])]

# 添加行索引
data = pd.DataFrame(stock_change, index=stock_code)

# 生成一个时间的序列，略过周末非交易日
column = pd.date_range('2017-01-01', periods=stock_change.shape[1], freq='B')

# index代表行索引，columns代表列索引
data = pd.DataFrame(stock_change, index=stock_code, columns=column)

print(stock_change)
print(data)

####################################################################################
### 索引操作
# 重置索引,drop=False
data.reset_index()

# 重置索引,drop=True
data.reset_index(drop=True)

data.set_index(keys)  # keys : 列索引名成或者列索引名称的列表

####################################################################################
#### series结构只有行索引
# 指定内容，默认索引
ps = pd.Series(np.arange(10))  # 索引:ps.index  值：ps.values
# 指定索引
pd.Series([6.7, 5.6, 3, 10, 2], index=[1, 2, 3, 4, 5])
# 通过字典数据创建
pd.Series({'red':100, 'blue':200, 'green': 500, 'yellow':1000})

####################################################################################
### 索引的操作
# 1.直接使用行列索引名字的方式（先列后行），不支持先行后列

# 2. 使用loc:只能指定行列索引的名字
data.loc['2018-02-27':'2018-02-22', 'open']

# 3.使用iloc可以通过索引的下标去获取 ： 获取前100天数据的'open'列的结果
data.iloc[0:100, 0:2].head()

# 4. 使用ix进行下表和名称组合做引
data.ix[0:4, ['open', 'close', 'high', 'low']]

# 5. 赋值和修改值
data['close'] = 1 or data.close = 1 # 智能操作列索引，如果使用行索引会再重新增加一列

####################################################################################
### 对values 或者index 进行排序

# 按照多个键进行排序
data = data.sort_values(by=['open', 'high'])

# 按照涨跌幅大小进行排序 , 使用ascending指定按照大小排序
data = data.sort_values(by='p_change', ascending=False).head()

# 对索引进行排序
data.sort_index()

# series排序时，只有一列，不需要参数
data['p_change'].sort_values(ascending=True).head()

####################################################################################
### 运算

#加上具体的一个数字
data['open'].add(1)

# 求出每天 close(收盘)- open(开盘)价格差
data['m_price_change'] = close.sub(open1)

# 逻辑判断的结果可以作为筛选的依据
data['p_change'] > 2

# 完成一个多个逻辑判断， 筛选p_change > 2并且open > 15
data[(data['p_change'] > 2) & (data['open'] > 15)] or data.query("p_change > 2 & turnover > 15")

# 可以指定值进行一个判断，从而进行筛选操作
data[data['turnover'].isin([4.19, 2.39])]

####################################################################################
### 统计运算
# 计算平均值、标准差、最大值、最小值
data.describe()

''' 对于单个函数去进行统计的时候，坐标轴还是按照这些默认为“columns” (axis=0, default)，如果要对行“index” 需要指定(axis=1) '''

# 使用统计函数：0 代表列求结果， 1 代表行求统计结果
data.max(0)

# 方差
data.var(0)

# 标准差
data.std(0)

# 中位数为将数据从小到大排列，在最中间的那个数为中位数。如果没有中间数，取中间两个数的平均值。
df = pd.DataFrame({'COL1' : [2,3,4,5,4,2],'COL2' : [0,1,2,3,4,2]})
df.median()

# 求出最大值的位置
data.idxmax(axis=0)

# 求出最小值的位置
data.idxmin(axis=0)

####################################################################################
### 累计统计函数

cumsum	 #计算前1/2/3/…/n个数的和
cummax	 #计算前1/2/3/…/n个数的最大值
cummin	 #计算前1/2/3/…/n个数的最小值
cumprod	 #计算前1/2/3/…/n个数的积

# 排序之后，进行累计求和
data = data.sort_index()
stock_rise = data['p_change']
# plot方法集成了前面直方图、条形图、饼图、折线图
stock_rise.cumsum()

'''
# 如果要使用plot函数，需要导入matplotlib.
import matplotlib.pyplot as plt
# plot显示图形
stock_rise.cumsum().plot()
# 需要调用show，才能显示出结果
plt.show()
'''

