# 原有的结构
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


# 需要的结构
# res = [{"subtype":[{'row_id': 1, 'weight': 10, 'type_name': '红色预警'},
#                     {'row_id': 2, 'weight': 8, 'type_name': '橙色预警'},
#                     {'row_id': 3, 'weight': 5, "type_name": "黄色预警"},
#                     {'row_id': 4, 'weight': 3, 'type_name': '蓝色预警'}],
#         "type_name":"预警数量"},.....]


# 方法一
from collections import defaultdict
temp_dict = defaultdict(list)
for item in data:
    type_name = item.pop('parent_type_name')
    temp_dict[type_name].append(item)

res = [dict(subtype=value, type_name=key) for key, value in temp_dict.items()]
print(res)


# 方法二
def group(data_list):
    d = {}
    for i in data_list:
        d.setdefault(i.pop("parent_type_name"), []).append(i)

    result = [{"type_name": k, "subtype": v} for k, v in d.items()]

    return result
print(group(data))