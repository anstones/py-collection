#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import time

class Siglenten():
	""" 单例模式 """
	def __init__(self):
		pass

	def __new__(cls, *args, **kwargs):
		if not hasattr(Siglenten, "_instance"):
			Siglenten._instance = object.__new__(cls, *args, **kwargs)
		return 	Siglenten._instance


# 使用装饰器实现单例模式
def singleton(cls, *args, **kwargs):
    instance = {}
    def _instance():
        if cls not in instance:
            instance[cls] = cls(*args, *kwargs)
        return instance[cls]
    return _instance

@singleton
class Test_singleton:
    def __init__(self):
        self.num = 0

    def add(self):
        self.num = 99

def fib(n):
	""" 斐波拉契 """
	a,b = 0,1
	while n>1:
		a,b = b, a+b
		n -= 1
		yield a

def wapper(func):
	""" 装饰器 """
	def inner(*args, **kwargs):
		start = time.time()
		func(*args, **kwargs)
		cost_time = "total cost:{}".format(time.time() - start)
		print(cost_time)
	return inner

def count_words(file_path):
	""" 统计文章内出现频率最高的10个词 """
	count = {}
	with open(file_path) as f:
		for line in f:
			words = line.strip().split()
			for word in words:
				if word in count:
					count[word] += 1
				else:
					count[word] = 1
	return sorted(count.items(), key = lambda k:k[1], reverse=True)[:11]

def binry_search(lists, item):
	""" 二分法：循环 """
	lists = sorted(lists)
	left, right = 0, len(lists)-1
	while left < right:
		middle = (left+right) // 2
		if lists[middle] < item:
			left = middle +1
		elif lists[middle] > item:
			right = middle
		else:
			return middle

def binry_search_1(lists, item, start=None, end=None):
	""" 二分法查找：递归 """
	start = start if start else 0
	end = end if end else len(lists)-1
	mid = (start+end)//2
	if start > end:
		return None
	if lists[mid] > item:
		return binry_search_1(lists, item, start, mid-1)
	elif lists[mid] < item:
		return binry_search_1(lists, item, mid+1, end)
	elif lists[mid] == item:
		return mid

def mop_sort(lists):
	""" 桶排序 """
	for i in range(len(lists)):
		for j in range(len(lists)-1 -i):
			if lists[j] > lists[j+1]:
				lists[j+1], lists[j] = lists[j], lists[j+1]
			else:
				pass
	return lists

def quick_start(li, start, end):
    """ 快速排序 """
    if start > end:
        return
    left = start
    right = end
    mid = li[start]
    while left < right:
        while left < right and li[right] >= mid:
            right -= 1
        li[left] = li[right]
        while left < right and li[left] <= mid:
            left += 1
        li[right] = li[left]
    li[left] = mid
    quick_start(li, start, right-1)
    quick_start(li, right+1, end)
