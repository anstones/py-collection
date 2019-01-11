#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
matplotlib.pie  饼图
plt.pie(x, labels=,autopct=,colors)
    x:数量，自动算百分比
    labels:每部分名称
    autopct:占比显示指定%1.2f%%
    colors:每部分颜色

plt.axis('equal') 保证长宽一样
"""

import matplotlib
from matplotlib.font_manager import *
from matplotlib import pyplot as plt

# 解决中文乱码
matplotlib.rcParams['axes.unicode_minus']=False
myfont = FontProperties(fname=r'C:\Users\Administrator\Desktop\mine\Project\project\NBA\simhei.ttf')

### 1. 需求：显示不同的电影的排片占比

# 1）准备数据
movie_name = ['雷神3：诸神黄昏','正义联盟','东方快车谋杀案','寻梦环游记','全球风暴','降魔传','追捕','七十七天','密战','狂兽','其它']

place_count = [60605,54546,45819,28243,13270,9945,7679,6799,6101,4621,20105]

# 2）创建画布
plt.figure(figsize=(20, 8), dpi=100)

# 3）绘制饼图
plt.pie(place_count, labels=movie_name, autopct="%1.2f%%", colors=['b','r','g','y','c','m','y','k','c','g','y'])

# 显示图例
plt.legend()

# 添加标题
plt.title("电影排片占比",fontproperties=myfont)

plt.axis('equal')

# 4）显示图像
plt.show()