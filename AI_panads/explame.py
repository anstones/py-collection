#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import pandas  as pd 
import numpy as np
from matplotlib import pyplot as plt
#文件的路径
path = "./IMDB-Movie-Data.csv"
#读取文件
df = pd.read_csv(path)

##############################################################################################
### Rating的分布情况

plt.figure(figsize=(20,8),dpi=80)
plt.hist(df["Rating"].values,bins=20)
# 求出最大最小值
max_ = df["Rating"].max()
min_ = df["Rating"].min()
# 修改刻度
plt.xticks(np.linspace(min_,max_,num=21))
# 添加网格
plt.grid()
plt.show()

##############################################################################################
### Runtime (Minutes)的分布情况

plt.figure(figsize=(20,8),dpi=80)
plt.hist(df["Runtime (Minutes)"].values,bins=20)
# 求出最大最小值
max_ = df["Runtime (Minutes)"].max()
min_ = df["Runtime (Minutes)"].min()
# 修改刻度
plt.xticks(np.linspace(min_,max_,num=21))
# 添加网格
plt.grid()
plt.show()


##############################################################################################
####统计电影分类(genre)的情况

# 进行字符串分割
temp_list = [i.split(",") for i in df["Genre"]]
# 获取电影的分类
genre_list = np.unique([i for j in temp_list for i in j]) 

# 1.增加新的列
temp_df = pd.DataFrame(np.zeros((df.shape[0],genre_list.shape[0])),columns=genre_list)
# 2.遍历每一部电影，temp_df中把分类出现的列的值置为1
for i in range(1000):
    #temp_list[i] ['Action','Adventure','Animation']
    temp_df.ix[i,temp_list[i]]=1
print(temp_df.sum().sort_values())
# 3、求和
# temp_df.sum().sort_values(ascending=False).plot(kind="bar",figsize=(20,8),fontsize=20,colormap="cool")
# print(temp_df)
