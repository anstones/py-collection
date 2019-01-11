#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
matplotlib.pyplot  折线图
figsize:指定图的长宽
    dpi:图像的清晰度
    返回fig对象
plt.xticks(x, **kwargs)
x:要显示的刻度值
plt.yticks(y, **kwargs)
y:要显示的刻度值

plt.grid(True, linestyle='--', alpha=0.5) 网格
"""
import matplotlib
from matplotlib.font_manager import *
from matplotlib import pyplot as plt
import random

# 解决中文乱码
matplotlib.rcParams['axes.unicode_minus']=False
myfont = FontProperties(fname=r'C:\Users\Administrator\Desktop\mine\Project\project\NBA\simhei.ttf')

### 1 初识matplotlib
'''
# 1）创建画布(容器层)
plt.figure(figsize=(10, 10))
# 2）绘制折线图(图像层)
plt.plot([1, 2, 3, 4, 5, 6 ,7], [17, 17, 18, 15, 11, 11, 13])
# 3）显示图像
plt.show()
'''


#### 2 需求：画出某城市11点到12点1小时内每分钟的温度变化折线图，温度范围在15度~18度
'''
# 准备x, y坐标的数据
x = range(60)
y_shanghai = [random.uniform(15, 18) for i in x]
# 增加北京的温度数据
y_beijing = [random.uniform(1, 3) for i in x]

# 1）创建画布
plt.figure(figsize=(20, 8), dpi=80)

# 2）绘制折线图
# plt.plot(x, y_shanghai)
plt.plot(x, y_shanghai, label="上海")
# 使用多次plot可以画多个折线
plt.plot(x, y_beijing, color='r', linestyle='--', label="北京")

# 显示图例
plt.legend(loc="best")

# 增加以下两行代码
# 构造x轴刻度标签
x_ticks_label = ["11点{}分".format(i) for i in x]
# 构造y轴刻度
y_ticks = range(40)

# 修改x,y轴坐标的刻度显示
plt.xticks(x[::5], x_ticks_label[::5],fontproperties=myfont)
plt.yticks(y_ticks[::5],fontproperties=myfont)

# 添加网格显示
plt.grid(True, linestyle='--', alpha=0.5)

# 添加x轴、y轴描述信息及标题
plt.xlabel("时间",fontproperties=myfont)
plt.ylabel("温度",fontproperties=myfont)
plt.title("中午11点0分到12点之间的温度变化图示",fontproperties=myfont)

# 3）显示图像
plt.show()
'''

### 3  上海和北京的天气图显示在同一个图的不同坐标系当中

# 准备x, y坐标的数据
x = range(60)
y_shanghai = [random.uniform(15, 18) for i in x]
# 增加北京的温度数据
y_beijing = [random.uniform(1, 3) for i in x]

# 1）创建画布
# plt.figure(figsize=(20, 8), dpi=80)
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 8), dpi=80)

# 2）绘制折线图
# plt.plot(x, y_shanghai)
# plt.plot(x, y_shanghai, label="上海")
axes[0].plot(x, y_shanghai, label="上海")
# 使用多次plot可以画多个折线
# plt.plot(x, y_beijing, color='r', linestyle='--', label="北京")
axes[1].plot(x, y_beijing, color='r', linestyle='--', label="北京")

# 显示图例
# plt.legend(loc="best")
axes[0].legend()
axes[1].legend()

# 增加以下两行代码
# 构造x轴刻度标签
x_ticks_label = ["11点{}分".format(i) for i in x]
# 构造y轴刻度
y_ticks = range(40)

# 修改x,y轴坐标的刻度显示
# plt.xticks(x[::5], x_ticks_label[::5])
# plt.yticks(y_ticks[::5])
axes[0].set_xticks(x[::5], x_ticks_label[::5])
axes[0].set_yticks(y_ticks[::5])
axes[1].set_xticks(x[::5], x_ticks_label[::5])
axes[1].set_yticks(y_ticks[::5])

# 添加网格显示
# plt.grid(True, linestyle='--', alpha=0.5)
axes[0].grid(True, linestyle='--', alpha=0.5)
axes[1].grid(True, linestyle='--', alpha=0.5)

# 添加x轴、y轴描述信息及标题
# plt.xlabel("时间")
# plt.ylabel("温度")
# plt.title("中午11点0分到12点之间的温度变化图示")
axes[0].set_xlabel("时间",fontproperties=myfont)
axes[0].set_ylabel("温度",fontproperties=myfont)
axes[0].set_title("上海中午11点0分到12点之间的温度变化图示",fontproperties=myfont)
axes[1].set_xlabel("时间",fontproperties=myfont)
axes[1].set_ylabel("温度",fontproperties=myfont)
axes[1].set_title("北京中午11点0分到12点之间的温度变化图示",fontproperties=myfont)

# 3）显示图像
plt.show()
