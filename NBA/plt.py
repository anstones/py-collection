import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.font_manager import *


matplotlib.rcParams['axes.unicode_minus']=False

myfont = FontProperties(fname=r'C:\Users\Administrator\Desktop\mine\Project\project\NBA\simhei.ttf')
# plt.rcParams['font.family'] = 'Microsoft Yahei'  # 字体，改为微软雅黑，默认 sans-serif
# plt.rcParams['font.size'] = 8  # 字体大小，整数字号，默认10


# df = pd.read_csv('./16-17Result.csv')  # 读取训练数据
df = pd.read_csv('./18-19Result.csv')  # 读取训练数据

df.index = range(1, len(df) + 1)  # set index from 1
pandas_index = df.index    # 将dataframe的索引赋给一个变量
df.insert(0, 'index', pandas_index)   # 第一个参数是列插入的位置
# print(df)

df_all = df[(df['win'] == 'Los Angeles Lakers') | (df['lose'] == "Los Angeles Lakers")] 


df_win = df_all[df_all["win"] == 'Los Angeles Lakers'] # 获胜概率大于5成
df_lose = df_all[df_all["win"] != 'Los Angeles Lakers'] # 获胜概率小于5成

df_lose["probability"] = 1 - df_lose["probability"] # 将获胜概率低于5成的比赛的获胜方改为骑士，失败方改为其他球队
df_lose["lose"] = df_lose["win"]
df_lose["win"] = "Los Angeles Lakers"

df3 = pd.merge(df_win, df_lose, how='outer')
df4 = df3.sort_values(by="index" , ascending=True)  # 按索引index排序，保证比赛顺序
# print(df4)

plt.figure(figsize=(40, 40))
clo = df4.iloc[:, 3]
y = clo.values.tolist()
cll = df4.iloc[:, 2]
team_list = cll.values.tolist()
x = []
for team in team_list:
    team = team.split(" ")[-1] 
    x.append(team)

plt.xlabel('球队', fontproperties=myfont)
plt.ylabel('获胜概率', fontproperties=myfont)
# plt.title('16-17赛季骑士获胜概率预测', fontproperties=myfont)
plt.title('18-19赛季湖人获胜概率预测', fontproperties=myfont)

x_axis = [i for i in range(1, len(x) + 1)]
plt.plot(x_axis, y)
plt.xticks(x_axis, x, rotation=90)
plt.savefig('./test2.png')
plt.grid(True) # 绘制网格
plt.show()
