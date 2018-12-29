import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.font_manager import *


matplotlib.rcParams['axes.unicode_minus']=False
myfont = FontProperties(fname=r'C:\Users\Administrator\Desktop\VS_code\Mydjango\NBA\simhei.ttf')
# plt.rcParams['font.family'] = 'Microsoft Yahei'  # 字体，改为微软雅黑，默认 sans-serif
# plt.rcParams['font.size'] = 8  # 字体大小，整数字号，默认10


df = pd.read_csv('./16-17Result.csv')  # 读取训练数据
df_all = df[(df['win'] == 'Cleveland Cavaliers') | (df['lose'] == "Cleveland Cavaliers")]


df_win = df_all[df_all["win"] == 'Cleveland Cavaliers']

df_lose = df_all[df_all["win"] != 'Cleveland Cavaliers']

df_lose["probability"] = 1 - df_lose["probability"]
df_lose["lose"] = df_lose["win"]
df_lose["win"] = "Cleveland Cavaliers"
df4 = pd.merge(df_win, df_lose, how='outer', on=None)
plt.figure(figsize=(40, 40))
clo = df4.iloc[:, 2]
y = clo.values.tolist()
cll = df4.iloc[:, 1]
team_list = cll.values.tolist()
x = []
for team in team_list:
    team = team.split(" ")[-1] 
    x.append(team)

plt.xlabel('球队', fontproperties=myfont)
plt.ylabel('获胜概率', fontproperties=myfont)
plt.title('16-17赛季骑士胜率预测', fontproperties=myfont)

x_axis = [i for i in range(1, len(x) + 1)]
plt.plot(x_axis, y)
plt.xticks(x_axis, x, rotation=90)
# plt.savefig('./test2.png')
plt.show()
