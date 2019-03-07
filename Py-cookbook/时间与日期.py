#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from datetime import datetime, date, timedelta
import calendar


# 查找星期中某一天最后出现的日期。
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday']


def get_previous_byday(dayname, start_date=None):
    if start_date is None:
        start_date = datetime.today()
    day_num = start_date.weekday()
    day_num_target = weekdays.index(dayname)
    days_ago = (7 + day_num - day_num_target) % 7
    if days_ago == 0:
        days_ago = 7
    target_date = start_date - timedelta(days=days_ago)
    return target_date

print(get_previous_byday('Wednesday'))


# 需要在当前月份中循环每一天
def get_month_range(start_date=None):
    if start_date is None:
        start_date = date.today().replace(day=1)
    _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
    end_date = start_date + timedelta(days=days_in_month)
    return (start_date, end_date)

a_day = timedelta(days=1)
text = '2019-02-1'
start_date = datetime.strptime(text, '%Y-%m-%d')
first_day, last_day = get_month_range(start_date)
while first_day < last_day:
     print(first_day)
     first_day += a_day
