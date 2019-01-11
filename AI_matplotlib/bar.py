#!/usr/bin/env python
# -*- encoding: utf-8 -*-

""" 
matplotlib.bar  柱状图 
color:选择柱状图的颜色
align:每个柱状图的位置对齐方式 :center,edge
width:柱状图的宽度
"""

import matplotlib
from matplotlib.font_manager import *
from matplotlib import pyplot as plt

# 解决中文乱码
matplotlib.rcParams['axes.unicode_minus']=False
myfont = FontProperties(fname=r'C:\Users\Administrator\Desktop\mine\Project\project\NBA\simhei.ttf')

### 1.需求-对比每部电影的票房收入
'''
movie_name = ['雷神3：诸神黄昏','正义联盟','东方快车谋杀案','寻梦环游记','全球风暴','降魔传','追捕','七十七天','密战','狂兽','其它']
# 横坐标
x = range(len(movie_name))
# 票房数据
y = [73853,57767,22354,15969,14839,8725,8716,8318,7916,6764,52222]

# 2）创建画布
plt.figure(figsize=(20, 8), dpi=100)

# 3）绘制柱状图
plt.bar(x, y, width=0.5, color=['b','r','g','y','c','m','y','k','c','g','b'])

# 修改x轴的刻度显示
plt.xticks(x, movie_name,fontproperties=myfont)

# 添加网格显示
plt.grid(linestyle="--", alpha=0.5)

# 添加标题
plt.title("电影票房收入对比",fontproperties=myfont)

# 4）显示图像
plt.show()
'''

### 2.需求-如何对比电影票房收入才更能加有说服力？

# 1）准备数据
movie_name = ['雷神3：诸神黄昏','正义联盟','寻梦环游记']

first_day = [10587.6,10062.5,1275.7]
first_weekend=[36224.9,34479.6,11830]

x = range(len(movie_name))

# 2）创建画布
plt.figure(figsize=(20, 8), dpi=100)

# 3）绘制柱状图
plt.bar(x, first_day, width=0.2, label="首日票房")
plt.bar([i+0.2 for i in x], first_weekend, width=0.2, label="首周票房")

# 显示图例
plt.legend()

# 修改x轴刻度显示
plt.xticks([i+0.1 for i in x], movie_name,fontproperties=myfont)

# 4）显示图像
plt.show()