#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import numpy as np
import pandas as pd

####################################################################################
### 文件的读取与保存

# 读取文件,并且指定只获取'open', 'high', 'close'指标
data = pd.read_csv("./stock_day/stock_day.csv", usecols=['open', 'high', 'close'])

# 保存csv文件
data[:10].to_csv("./test.csv", columns=['open'], index=False, mode='a', header=False)
'''
dataFrame.to_csv(path_or_buf=None, sep=', ’, columns=None, header=True, index=True, index_label=None, mode='w', encoding=None)
params:
        path_or_buf :path
        sep : default ‘,’
        columns :sequence, optional
        mode:'w'：重写, 'a' 追加
        index:是否写进行索引
        header :boolean or list of string, default True,是否写进列索引值
'''

# HDF5在存储的是支持压缩，使用的方式是blosc，这个是速度最快的也是pandas默认支持的，HDF5还是跨平台的，可以轻松迁移到hadoop 上面
# 存储文件
data.to_hdf("./test.h5", key="day_high")
# 保存文件
new_data = pd.read_hdf("./test.h5", key="day_high")

####################################################################################
### pandas 缺失值操作
# 判断数据是否为NaN：
pd.isnull(data)
pd.notnull(data)

# 删除存在缺失值的:
data.dropna(axis='rows')  # 注：不会修改原数据，需要接受返回值
data.fillna(value, inplace=True)  # value:替换成的值 ; inplace:True:会修改原数据，False:不替换修改原数据，生成新的对象

# replace替换具体某些值的思路
'''
1、先替换‘?’为np.nan
wis = wis.replace(to_replace='?', value=np.nan)
2、在进行缺失值的处理
wis = wis.dropna()
'''

####################################################################################

### 数据离散化： 对数据进行阶段性分组，并统计个数,一般会与value_counts搭配使用，统计每组的个数
p_change= data['p_change']
qcut = pd.qcut(p_change, 10)
# 计算分到每个组数据个数
qcut.value_counts()


# 自己指定分组区间
bins = [-100, -7, -5, -3, 0, 3, 5, 7, 100]
p_counts = pd.cut(p_change, bins)


# 得出one-hot编码矩阵
dummaries = pd.get_dummies(p_counts, prefix="rise")  # prefix:分组名字

####################################################################################
### 合并
# 按照行索引进行， 一般应用在行或者列相同的场景 axis=1 行索引；axis=0 列索引 
pd.concat([data, dummaries], axis=1) 

# 默认内连接
result = pd.merge(left, right, on=['key1', 'key2'])


####################################################################################
### 交叉表的实现（crosstab/pivot_table）

# 寻找星期几跟股票涨跌的关系
# 1、先根据对应的日期找到星期几
date = pd.to_datetime(data.index).weekday
data['week'] = date
# 2、把p_change按照大小分类，以0为界限
data['posi_neg'] = np.where(data['p_change'] > 0, 1, 0)
# 通过交叉表找寻两列数据的关系
count = pd.crosstab(data['week'], data['posi_neg'])
# 算数运算，先求和
count.sum(axis=1).astype(np.float32)
# 进行相除操作，得出比例
pro = count.div(count.sum(axis=1).astype(np.float32), axis=0)

# pivot_table
data.pivot_table(['posi_neg'], index=['week'])
