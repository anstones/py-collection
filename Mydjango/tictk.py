#!/usr/bin/python
#-*- coding:utf-8 –*-

"""Train tickets query via command-line.

Usage:
    docoptTest [-gdtkz] <from> <to> <date>

Options:
     -h, --help 显示帮助菜单
     -g         高铁
     -d         动车
     -t         特快
     -k         普快
     -z         直达

Example:
    docoptTest  beijing shanghai 2016-09-26
"""

from docopt import docopt
from prettytable import PrettyTable
import re
"""Train tickets query via command-line.

Usage:
    docoptTest [-gdtkz] <from> <to> <date>

Options:
     -h, --help 显示帮助菜单
     -g         高铁
     -d         动车
     -t         特快
     -k         普快
     -z         直达

Example:
    docoptTest  beijing shanghai 2016-09-26
"""

from docopt import docopt
from prettytable import PrettyTable
import re
import requests
import sys

class TrainCollection(object):
    # 显示车次、起始车站、出发-到达时间、历时、二等座、软卧、软座、硬卧、硬座、无座
    header = 'Train Station Time Duration Sec Soft Hard Sit NoSit'.split()

    def __init__(self, rows, date, count):
        self.rows = rows
        self.date = date
        self.count = count

    def _get_duration(self, row):
        #获取车次运行时间
        duration = row.get('lishi').replace(':', 'h') +'m'
        if duration.startswith('00'):
            duration = duration[3:]
        elif duration.startswith('0'):
            duration = duration[1:]
        dif = row.get('day_difference')
        if dif == "0":
            duration = '\n'.join([duration,"today"])
        else:
            duration = '\n'.join([duration,"tommorrow"])
        return duration


    def _get_num(self, row, type, response, re_type):
        #获取余票数目
        num = row.get(type)
        if num == "--":
            return num
        elif num.isdigit() == False:
            return 0
        else:
            price = response[re_type].decode('utf-8').encode('gbk','ignore')
            return '\n'.join([num,"".join(["$",price])])

    @property
    def trains(self):
        for row in self.rows:
            url = "https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no={}&from_station_no={}&to_station_no={}&seat_types={}&train_date={}"\
                    .format(row['train_no'], row['from_station_no'],row['to_station_no'],row['seat_types'],self.date)

            if self.count == "00000" or (self.count[0]=="1" and row['station_train_code'].startswith("D")) or (self.count[1]=="1" and row['station_train_code'].startswith("G")) or (self.count[2]=="1" and row['station_train_code'].startswith("K")) or (self.count[3]=="1" and row['station_train_code'].startswith("T")) or (self.count[4]=="1" and row['station_train_code'].startswith("Z")):
                r = requests.get(url, verify=False).json()['data']
                #print r['A2'].decode('utf-8').encode('gbk','ignore')

                train = [
                    #车次
                    row['station_train_code'],
                    #起点-终点
                    ("\n").join([row['from_station_name'],row['to_station_name']]),
                    #出发-到达时间
                    '\n'.join([row['start_time'], row['arrive_time']]),
                    #历时
                    self._get_duration(row),
                    #二等座
                    self._get_num(row, 'ze_num', r, 'O'),
                    #软座
                    self._get_num(row, 'rz_num', r, 'A2'),
                    #硬卧
                    self._get_num(row, 'yw_num', r, 'A3'),
                    #硬座
                    self._get_num(row, 'yz_num', r, 'A1'),
                    #无座
                    self._get_num(row, 'wz_num', r, 'WZ')
                ]
                yield train
            else:
               return

    def pretty_print(self):
        '''
        数据已经获取到了，剩下的就是提取我们要的信息并将它显示出来
        prettytable这个库可以让我们像MySQL数据库那样格式化显示数据
        '''
        pt = PrettyTable()
        #设置每一列的标题
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)


#get stations
def parseStation():
    url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8955"
    r = requests.get(url, verify=False)
    stations = re.findall(r'([A-Z]+)\|([a-z]+)', r.text)
    stations = dict(stations)
    stations = dict(zip(stations.values(), stations.keys()))
    return stations

#修改字体颜色
def colored(color, text):
    table = {
        'red': '\033[91m',
        'green': '\033[92m',
        # no color
        'nc': '\033[0m'}
    cv = table.get(color)
    nc = table.get('nc')
    return ''.join([cv, text, nc])

#main func
def cli():

    #获取参数
    arguments = docopt(__doc__)
    all_code = parseStation()
    #print arguments

    from_station = all_code.get(arguments['<from>'])
    to_station = all_code.get(arguments['<to>'])
    date = arguments['<date>']
    #print "date=",date,";to_station=",to_station,";from_station=",from_station

    count = "00000"
    s="1"
    if arguments['-d']==True: count = s + count[1:]
    if arguments['-g']==True: count = count[0] + s + count[2:]
    if arguments['-k']==True: count = count[0:2] + s + count[3:]
    if arguments['-t']==True: count = count[0:3] + s + count[4]
    if arguments['-z']==True: count = count[0:4] + s 
    #print count

    #构建URL
    # url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'\
    #     .format(date, from_station, to_station)
    url = 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs={}&ts={}&date={}&flag=N,N,Y'.format(from_station, to_station, date)

    res = requests.get(url, verify=False)
    print('res == %s'%res.url)
    r = res.json()

    #处理返回JSON数据
    if r == -1:
        msg = '%s\n输入格式有误！' % arguments
        print (msg.decode('utf-8'))

    elif r['data']['flag'] == False:   
        msg = '%s从%s到%s，没有符合条件的数据！' % (date,arguments['<from>'],arguments['<to>'])
        print (msg.decode('utf-8'))

    else:
        rows = r['data']['datas']
        trains = TrainCollection(rows,date,count)
        trains.pretty_print()

if __name__ == "__main__":
    cli()