# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# 微信好友信息
import re
import itchat
from pyecharts import Page, Pie, Map, Bar


# 实现获取朋友指定信息的方法
def get_key_info(friends_info, key):
    return list(map(lambda friend_info: friend_info.get(key), friends_info))


# 获取朋友的相关信息，生成一个 {key:[value1,value2,...],} 类型的字典，最后返回该字典
def get_friends_info(friends):
    friends_info = dict(
        sex=get_key_info(friends, 'Sex'),              # 性别
        province=get_key_info(friends, 'Province'),    # 省份
        city=get_key_info(friends, 'City')             # 城市
    )
    return friends_info


# 处理数据
def count_nums(new_list):
    new_dict = {}
    for i in new_list:
        if bool(re.search('[a-z]|[A-Z]', i)):   # 如果带英文字母（要么是国外，要么是乱写的）就跳出本次循环
            continue
        elif not new_dict.__contains__(i):
            new_dict[i] = 1
        else:
            new_dict[i] += 1
    new_dict.pop('')   # 去掉空的键
    return new_dict


# 画出男女性别比例折线图、朋友省级分布图、城市Top10图
def analysis(friends):
    friends_info = get_friends_info(friends)

    # 男女性别比例
    sex_list = friends_info['sex']
    from collections import Counter
    sex_dict = dict(Counter(sex_list))
    attr = ["未知", "男性", "女性"]
    value = [sex_dict[0], sex_dict[1], sex_dict[2]]
    page = Page()
    chart1 = Pie("微信好友性别比例图",title_pos='center')
    chart1.add("", attr, value, is_label_show=True, legend_orient="vertical", legend_pos="left")
    page.add(chart1)

    # 中国省级分析
    province_list = friends_info['province']
    province_dict = count_nums(province_list)
    attr, value = list(province_dict.keys()), list(province_dict.values())
    # 中国省级分析画图
    chart2 = Map('好友省级分布(中国地图)', width=1200, height=600)
    chart2.add('', attr, value, maptype='china', is_label_show=True, is_visualmap=True, visual_text_color='#000')
    page.add(chart2)

    # 中国城市分析(取前10个人数最多的城市)
    city_list = friends_info['city']
    city_dict = count_nums(city_list)
    top_ten_city = dict(sorted(city_dict.items(), key=lambda x: x[1], reverse=True)[0:10])
    attr, value = list(top_ten_city.keys()), list(top_ten_city.values())
    # 中国城市分析画图
    chart3 = Bar('好友城市分布Top10柱状图', width=900, height=500)
    chart3.add('', attr, value, is_stack=False,is_label_show=True,bar_category_gap='20%')
    page.add(chart3)

    page.render('analysisResult.html')


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    friends = itchat.get_friends(update=True)

    analysis(friends)

    #itchat.logout()