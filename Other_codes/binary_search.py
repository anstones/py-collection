# -*- coding: utf-8 -*-

# 二分法查找，返回所查询的数值对应下标
def binary_search(order_list,item):
    low = 0
    high = len(order_list)-1

    while high-low>1:
        middle = (low+high)//2
        if order_list[middle]<item:
            low = middle+1
        elif order_list[middle]>item:
            high = middle-1
        else:
            return middle

    if high-low==1:
        if order_list[low]==item:
            return low
        if order_list[high]==item:
            return high
    if high-low==0:
        return high


"""
递归二分法查找
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