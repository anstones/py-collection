from datetime import datetime
import pandas as pd

def last_day_of_month(any_day):
    """
    获取获得一个月中的最后一天
    :param any_day: 任意日期
    :return: string
    """
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


def get_open_day_list(year=None, month=None, day=None):
    """
    获取某月的开盘日,可扩展为获取全年开盘日期
    :param year 年
    :param month 月
    :param day 日
    :return 开盘日列表
    """
    year = year if year else datetime.now().year
    month = month if month else datetime.now().month-1
    day = day if day else datetime.now().day

    # startdate = "{}-{}-1".format(year, month)
    startdate = '2019-10-01'
    # enddate = last_day_of_month(datetime.date(year, month, day))
    enddate = '2019-10-31'
    holiday = ['10-01', '10-02', '10-03', '10-04', '10-05', '10-06', '10-07']

    datalist = list(pd.date_range(start=startdate, end=enddate))
    df = pd.DataFrame({'date':datalist})

    df['month'] = df['date'].apply(lambda x: x.month)
    df['day'] = df['date'].apply(lambda x: x.day) 
    df['weekday'] = df['date'].apply(lambda x: x.weekday()+1)

    # 工作日与休息日
    isrest = ((df['weekday'] == 6) | (df['weekday'] == 7))
    df['label'] = isrest*1

    print(df)

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
    print(da)
    # 活得开盘日期列表
    result = []
    for i in da:
        if i["label"] == 0:
            result.append(i["10_date"])
    print(result)
    return result
