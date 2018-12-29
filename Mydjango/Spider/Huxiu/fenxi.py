import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


plt.style.use('ggplot')
fig= plt.figure(figsize=(8,5))
# fig,ax = plt.subplots(figsize=(16,9))
ax1 = fig.add_subplot(1,1,1)
colors = '#6D6D6D'  #设置标题颜色为灰色
color_line = '#CC2824'
# colors = '#242424'  #设置标题颜色为灰色
fontsize_title = 20
fontsize_text = 10


connection = pymysql.connect(host='localhost'
                             , port=3306
                             , db='mine'
                             , user='root'
                             , passwd='mysql'
                             , charset='utf8')

sql = 'select * from huxiu_db'
data = pd.read_sql(sql, connection)

# print(data.shape)  # 查看行数和列数

# 删除无用_id列
data.drop(['id'],axis=1,inplace=True)
# 替换掉特殊字符©
data['name'].replace('©','',inplace=True,regex=True)
# 字符更改为数值
data = data.apply(pd.to_numeric,errors='ignore')
# 更该日期格式
data['write_time'] = data['write_time'].replace('.*前','2018-10-31',regex=True)

# 为了方便，将write_time列，包含几小时前和几天前的行，都替换为10月31日最后1天。
data['write_time'] = pd.to_datetime(data['write_time'])

# 判断整行是否有重复值
# print(any(data.duplicated()))
# 显示True，表明有重复值，进一步提取出重复值数量
data_duplicated = data.duplicated().value_counts()
# print(data_duplicated) # 显示2 True ，表明有2个重复值
# 删除重复值
data = data.drop_duplicates(keep='first')
# 删除部分行后，index中断，需重新设置index
data = data.reset_index(drop=True)


data['title_length'] = data['title'].apply(len)
data['year'] = data['write_time'].dt.year

# print(data.shape)
# print(data.describe())
# print(data['name'].describe())
# print(data['write_time'])


def analysis1(data):
    # # 汇总统计
    # print(data.describe())
    # print(data['name'].describe())
    # print(data['write_time'].describe())

    data.set_index(data['write_time'], inplace=True)
    data = data.resample('Q').count()['name']  # 以季度汇总
    data = data.to_period('Q')
    # 创建x,y轴标签
    x = np.arange(0, len(data), 1)
    ax1.plot(x, data.values,  # x、y坐标
             color=color_line,  # 折线图颜色为红色
             marker='o', markersize=4  # 标记形状、大小设置
             )
    ax1.set_xticks(x)  # 设置x轴标签为自然数序列
    ax1.set_xticklabels(data.index)  # 更改x轴标签值为年份
    plt.xticks(rotation=90)  # 旋转90度，不至太拥挤

    for x, y in zip(x, data.values):
        plt.text(x, y + 10, '%.0f' % y, ha='center', color=colors, fontsize=fontsize_text)
        # '%.0f' %y 设置标签格式不带小数
    # 设置标题及横纵坐标轴标题
    plt.title('虎嗅网文章数量发布变化(2012-2018)', color=colors, fontsize=fontsize_title)
    plt.xlabel('时期')
    plt.ylabel('文章(篇)')
    plt.tight_layout()  # 自动控制空白边缘
    plt.savefig('虎嗅网文章数量发布变化.png', dpi=200)
    plt.show()


def analysis2(data):
    # # 总收藏排名
    # top = data.sort_values(['favorites'],ascending = False)
    # # 收藏前10
    # top.index = (range(1,len(top.index)+1)) # 重置index，并从1开始编号
    # print(top[:10][['title','favorites','comment']])

    # 按年份排名
    # # 增加一列年份列
    # data['year'] = data['write_time'].dt.year
    def topn(data):
        top = data.sort_values('favorites',ascending=False)
        return top[:3]
    data = data.groupby(by=['year']).apply(topn)
    print(data[['title','favorites']])
    # 增加每年top123列，列依次值为1、2、3
    data['add'] = 1 # 辅助
    data['top'] = data.groupby(by='year')['add'].cumsum()
    data_reshape = data.pivot_table(index='year',columns='top',values='favorites').reset_index()
    # print(data_reshape)  # ok
    data_reshape.plot(
        # x='year',
        y=[1,2,3],
        kind='bar',
        width=0.3,
        color=['#1362A3','#3297EA','#8EC6F5']  # 设置不同的颜色
        # title='虎嗅网历年收藏数最多的3篇文章'
        )
    plt.xlabel('Year')
    plt.ylabel('文章收藏数量')
    plt.title('历年 TOP3 文章收藏量比较',color = colors,fontsize=fontsize_title)
    plt.tight_layout()  # 自动控制空白边缘，以全部显示x轴名称
    # plt.savefig('历年 Top3 文章收藏量比较.png',dpi=200)
    plt.show()



if __name__ == '__main__':
    analysis2(data)