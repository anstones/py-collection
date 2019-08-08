#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
衡量两个变量的相关程度
"""

import numpy as np
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from scipy.stats import ttest_ind

x = np.random.normal(0,1,500) # 从-1到1生成随机数
y1 = np.random.normal(0,1,500) # 均值为0，方差为1的一组数
y2 = np.random.normal(0,100,500) # 均值为0，方差为10的一组数

print("----------------pearson----------------")
r1, p1 = pearsonr(x,y1)
print("r1 = ",r1)
print("p1 = ",p1)

#y2相比于y1,方差更大，混乱程度更高，与相x1的相关性越差
r2, p2 = pearsonr(x,y2)
print("r2 = ",r2) #[-1,1],绝对值约大越相关，正为正相关，负为负相关，为0时不相关
print("p2 = ",p2) #恒为非负，越大越相关，500个样本以上有较高可靠性
print("----------------spearman---------------")

c1, pv1 = spearmanr(x,y1)
print("c1 = ",c1)
print("pv1 = ",pv1)

#y2相比于y1,方差更大，混乱程度更高，与相x1的相关性越差
c2, pv2 = spearmanr(x,y2)
print("c2 = ",c2) #[-1,1],绝对值约大越相关，正为正相关，负为负相关，为0时不相关
print("pv2 = ",pv2) #恒为非负，越大越相关，500个样本以上有较高可靠性

#显著性检验
stat_val, p_val = ttest_ind(x, y1, equal_var=False)
print("----------------P-----------------------")
print("stat_val = ",stat_val) #相关性
print("p_val = ",p_val) #是否显著 &lt;0.05为显著性
