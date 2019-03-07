import heapq

from collections import defaultdict,OrderedDict


# 查找序列内最大和最小的N个数
portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
    {'name': 'FB', 'shares': 200, 'price': 21.09},
    {'name': 'HPQ', 'shares': 35, 'price': 31.75},
    {'name': 'YHOO', 'shares': 45, 'price': 16.35},
    {'name': 'ACME', 'shares': 75, 'price': 115.65}
]
cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
print(cheap)
expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])
print(expensive)



prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}
d = defaultdict(list)
for key, value in prices.items():
    d[key].append(value)
print(d)


min_price = min(zip(prices.values(), prices.keys()))
print(min_price)
max_price = max(zip(prices.values(), prices.keys()))
print(max_price)


words = [
    'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
    'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
    'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
    'my', 'eyes', "you're", 'under'
]
from collections import Counter
word_counts = Counter(words)
# 出现频率最高的3个单词
top_three = word_counts.most_common(3)
print(top_three)
# Outputs [('eyes', 8), ('the', 5), ('look', 4)]


rows = [
    {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
    {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
    {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
    {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
]
from operator import itemgetter
# 根据字典的某个或者多个键排序
rows_by_fname = sorted(rows, key=itemgetter('fname'))
rows_by_uid = sorted(rows, key=itemgetter('uid'))
rows_by_lfname = sorted(rows, key=itemgetter('lname','fname'))
print(rows_by_fname)
print(rows_by_uid)


data = [
    {'row_id': 1, 'weight': 10, 'type_name': '红色预警', 'parent_type_name': '预警数量'}, 
    {'row_id': 2, 'weight': 8, 'type_name': '橙色预警', 'parent_type_name': '预警数量'}, 
    {'row_id': 3, 'weight': 5, "type_name": "黄色预警", 'parent_type_name': '预警数量'}, 
    {'row_id': 4, 'weight': 3, 'type_name': '蓝色预警', 'parent_type_name': '预警数量'}, 
    {'row_id': 5, 'weight': 10, "type_name": "红色预警",'parent_type_name': '预警处置率'}, 
    {'row_id': 6, 'weight': 8, 'type_name': '橙色预警', 'parent_type_name': '预警处置率'}, 
    {'row_id': 7, 'weight': 5, 'type_name': '黄色预警','parent_type_name': '预警处置率'}, 
    {'row_id': 8, 'weight': 3, 'type_name': '蓝色预警', 'parent_type_name': '预警处置率'}, 
    {'row_id': 9, 'weight': 8, 'type_name': '巡更延迟','parent_type_name': '巡更异常'}, 
    {'row_id': 10, 'weight': 8, 'type_name': '巡更漏巡', 'parent_type_name': '巡更异常'},
    {'row_id': 11, 'weight': 10, 'type_name': '访客人员','parent_type_name': '外来人员'},
    {'row_id': 12, 'weight': 10, 'type_name': '访客车辆', 'parent_type_name': '外来人员'}, 
    {'row_id': 13, 'weight': 3, 'type_name': '/', 'parent_type_name': '重点人员'}, 
    {'row_id': 14, 'weight': 3, 'type_name': '人防', 'parent_type_name': '三防数据'}, 
    {'row_id': 15, 'weight': 3, 'type_name': '物防', 'parent_type_name': '三防数据'},
    {'row_id': 16, 'weight': 3, 'type_name': '技防', 'parent_type_name': '三防数据'}]

from itertools import groupby
from operator import itemgetter

data.sort(key=itemgetter('parent_type_name'))
# Iterate in groups
data = []

for date, items in groupby(data, key=itemgetter('parent_type_name')):
    print(date)
    for i in items:
        i.pop("parent_type_name")
        print(i)


values = ['1', '2', '-3', '-', '4', 'N/A', '5']
def is_int(val):
    try:
        x = int(val)
        return True
    except ValueError:
        return False
ivals = list(filter(is_int, values))
print(ivals)


addresses = [
    '5412 N CLARK',
    '5148 N CLARK',
    '5800 E 58TH',
    '2122 N CLARK',
    '5645 N RAVENSWOOD',
    '1060 W ADDISON',
    '4801 N BROADWAY',
    '1039 W GRANVILLE',
]
counts = [ 0, 3, 10, 4, 1, 7, 6, 1]

from itertools import compress
more5 = [n > 5 for n in counts]
li = list(compress(addresses, more5))
print(li)


prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}

p1 = {key: value for key, value in prices.items() if value > 200}
print(p1)
tech_names = {'AAPL', 'IBM', 'HPQ', 'MSFT'}
p2 = {key: value for key, value in prices.items() if key in tech_names}
print(p2)


from collections import namedtuple
# 命名元祖，解决数据库查询结果比较大，可以替换下标操作（下标操作严重依赖于数据结构，最好不用）
Stock = namedtuple('Stock', ['name', 'shares', 'price'])
def compute_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price
    return total


s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
the eyes, not around the eyes, don't look around the eyes, \
look into my eyes, you're under."

import textwrap
# 指定列宽
print(textwrap.fill(s, 30))