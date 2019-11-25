# -*- coding: utf-8 -*-

# 二分法查找，返回所查询的数值对应下标
def binary_search(lists,item):
    """ 二分法查找:循环 """
    num_list = sorted(lists)
    left, right = 0, len(num_list)

    while left < right:
    	middle = (left + right) // 2
    	if lists[middle] < item:
    		left = middle +1
    	elif lists[middle] > item:
    		right = middle
    	else:
    		return "待查元素{}在列表中下标为{}".format(item, middle)    
    return "待查元素{}不在列表中".format(item)


"""
递归二分法查找：递归
"""
def func(l, value, start=None, end=None):
    start = start if start else 0
    end = end if end else len(l)-1
    if start <= end:
        mid = start+end // 2
        if l[mid] == value:
            return mid
        elif l[mid] > value:        
            return func(l, value, start, mid-1)
        else:
            return func(l, value, mid+1, end)
    else:
        return None
    

order_list = [2,3,4,6,89,99]
item =2
print(binary_search(order_list,item))
item =3
print(binary_search(order_list,item))
item =4
print(binary_search(order_list,item))
item =6
print(binary_search(order_list,item))
item =89
print(binary_search(order_list,item))
item =99
print(binary_search(order_list,item))


l1 = ['b','c','d','b','c','a','a']
l2 = []
[l2.append(i) for i in l1 if not i in l2]
print (l2)