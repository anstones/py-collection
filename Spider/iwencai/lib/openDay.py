# -*- coding: utf-8 -*-

import datetime
import calendar
import pandas as pd
from datetime import timedelta

init_date = datetime.date.today()
now = datetime.datetime.now()

def last_day_of_month(any_day):
    """
    获取一个月中的最后一天
    :param any_day: 任意日期
    :return: string
    """
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


def day_of_pre_month():
    """
    给定时间前月最后一天
    """
    current_month_first_day = datetime.date(year=init_date.year, month=init_date.month, day=1)
    last_day_of_pre_month = current_month_first_day - datetime.timedelta(days=1)
    first_day_of_pre_month = datetime.date(last_day_of_pre_month.year, last_day_of_pre_month.month, 1)
    return first_day_of_pre_month, last_day_of_pre_month

def daf_of_fre_month():
    """
    今天之前的一个月
    """
    current_month_day = datetime.date(year=init_date.year, month=init_date.month-1, day=init_date.day)
    today = datetime.date.today()
    return current_month_day, today

def day_of_pre_yaer():
    """
    去年
    """
    this_year_start = datetime.datetime(now.year, 1, 1)
    last_year_end = this_year_start - timedelta(days=1)
    last_year_start = datetime.datetime(last_year_end.year, 1, 1)
    return last_year_start.strftime("%Y-%m-%d"), last_year_end.strftime("%Y-%m-%d")

def day_of_fre_yaer():
    """
    今天之前的一年
    """
    first_day_of_this_year = datetime.date(init_date.year, 1, 1)
    last_day_of_last_year = first_day_of_this_year - datetime.timedelta(days=1)
    same_day_of_last_year = datetime.date(last_day_of_last_year.year, init_date.month, init_date.day)
    return same_day_of_last_year.strftime("%Y-%m-%d"), init_date

def day_of_current():
    """ 今年 """
    this_year_start = datetime.datetime(now.year, 1, 1)
    this_year_start = this_year_start.strftime("%Y-%m-%d")
    this_year_end = datetime.datetime(now.year + 1, 1, 1) - timedelta(days=1)
    return this_year_start, init_date

def parase_params(params):
    """ 
    根据参数判断需要抓取的时间 
    :params = None 获取10月份涨停数据
    :params = 1    获取上个月涨停数据
    :params = 2    获取前一个月涨停数据
    :params = 3    获取去年所有数据
    :params = 4    获取前一年所有数据
    :params = 5    获取今年数据
    """
    if params == 0:
        startdate, enddate = '2019-10-01', '2019-10-31'
    elif params == 1:
        startdate, enddate = day_of_pre_month()
    elif params == 2:
        startdate, enddate = daf_of_fre_month()
    elif params == 3:
        startdate, enddate = day_of_pre_yaer()
    elif params == 4:
        startdate, enddate = day_of_fre_yaer()
    elif params == 5:
        startdate, enddate = day_of_current()
    return startdate, enddate

def get_open_day_list(params=None):
    """
    获取某月的开盘日,可扩展为获取全年开盘日期
    :param  参数
    :return 开盘日列表
    """
    startdate, enddate = parase_params(params)
    holiday = ['01-01', '05-1', '10-01', '10-02', '10-03', '10-04', '10-05', '10-06', '10-07']
    print("you will get the data from {} to {}".format(startdate, enddate))

    datalist = list(pd.date_range(start=startdate, end=enddate))
    df = pd.DataFrame({'date':datalist})

    df['month'] = df['date'].apply(lambda x: x.month)
    df['day'] = df['date'].apply(lambda x: x.day) 
    df['weekday'] = df['date'].apply(lambda x: x.weekday()+1)

    # 工作日与休息日
    isrest = ((df['weekday'] == 6) | (df['weekday'] == 7))
    df['label'] = isrest*1

    # 节假日
    for h in holiday:
        h_month,h_day = h.split('-')
        h_index = ((df['month'] == int(h_month)) & (df['day'] == int(h_day)))
        df.loc[h_index, 'label'] = 2

    # 日期列格式化  表示列
    df['10_date'] = df['date'].apply(lambda x : x.strftime('%m-%d'))
    new_df = df[['10_date','label']]

    # 转化为字典
    da = new_df.to_dict(orient='records')
    # 活得开盘日期列表
    result = []
    for i in da:
        if i["label"] == 0:
            result.append(i["10_date"])
    print("open day:{}".format(result))
    return result

def main():
    get_open_day_list()


if __name__ == "__main__":
    main()
