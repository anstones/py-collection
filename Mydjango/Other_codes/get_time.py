#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import re

result_r = []
result_t = []


def get_time_list(path):
    time_list = []
    with open(r"{}".format(path), encoding='utf-8') as f:
        data_str = f.read()
        # print(data_str)
        findword = u"(.+the algo cost:.+)"  # .+表示匹配有字段ReceiveAccount这一行所有数据
        pattern = re.compile(findword)
        results = pattern.findall(data_str)
        print(results)
        if results:
            for result in results:
                res = result.split(":")[-1]
                if 'e' not in res:
                    res_f = float(res)
                    if res_f < 2 and res_f > 0.2:
                        print(res_f)
                        time_list.append(res_f)
        else:
            return
    return time_list


def averagenum(num):
    nsum = 0
    for i in range(len(num)):
        nsum += num[i]
    return nsum / len(num)


total_time = {}
for i in range(1, 4):
    path = 'proxy_8888_logger.log.{}'.format(i)
    time_list = get_time_list(path)
    time1 = averagenum(time_list)
    time = round(time1,3)
    print("第%s 循环：%s"%(i,time))
    total_time[i] = time
    print(total_time)

time = []
for value in total_time.values():
    time.append(value)


print(averagenum(time))
