#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import csv
import codecs

def get_result():
    with open(r"17-18_result.csv", 'r')as f:
        for line in f:
            a = ''
            if 'PTS' not in line:
                line_list = line.split(",")
                v_team = line_list[2]
                v_PTS = int(line_list[3])
                h_team = line_list[4]
                h_PTS = int(line_list[5])
                if v_PTS > h_PTS: # 客队胜
                    a_obj = {"WTeam":v_team,"LTeam":h_team,"WLoc":"V"}
                    a = json.dumps(a_obj) + ',\n'
                if h_PTS > v_PTS: # 主队胜
                    a_obj = {"WTeam":h_team,"LTeam":v_team,"WLoc":"H"}
                    a = json.dumps(a_obj) + ',\n'

            with open(r'17-18result.json','a') as f2:
                f2.write(a)


def get_schedule():
    with open(r"18-19schedule.csv", 'r')as f:
        for line in f:
            a = ''
            if 'PTS' not in line:
                line_list = line.split(",")
                print(line_list)
                v_team = line_list[2]
                
                h_team = line_list[4]
                a_obj = {"Vteam":v_team,"Hteam":h_team}
                a = json.dumps(a_obj) + ',\n'

            with open(r'18-19_Schedule.json','a') as f2:
                f2.write(a)


def json2csv(path):
    jsonData = codecs.open(path+'.json', 'r', 'utf-8')
    # csvfile = open(path+'.csv', 'w') # 此处这样写会导致写出来的文件会有空行
    # csvfile = open(path+'.csv', 'wb') # python2下
    csvfile = open(path+'.csv', 'w', newline='') # python3下
    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
    flag = True
    for line in jsonData:
        json_str = line[0:-3]
        dic = json.loads(json_str)
        if flag:
            # 获取属性列表
            keys = list(dic.keys())
            print (keys)
            writer.writerow(keys) # 将属性列表写入csv中
            flag = False
        # 读取json数据的每一行，将values数据一次一行的写入csv中
        writer.writerow(list(dic.values()))
    jsonData.close()
    csvfile.close()


if __name__ == '__main__':
    # get_result()
    # get_schedule()
    path = '17-18result'
    # path = '18-19_Schedule'
    json2csv(path)



