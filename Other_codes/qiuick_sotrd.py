#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# 快速排序
def quick_sort(li, start, end):
    if start >= end:
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
    quick_sort(li, start, left - 1)
    quick_sort(li, left + 1, end)

# 递归实现快排
def quicksort(array):
    less = []
    greater = []
    if len(array) <= 1:
            return array
    pivot = array.pop()
    for x in array:
        if x <= pivot: 
            less.append(x)
        else: 
            greater.append(x)
    return quicksort(less) + [pivot] + quicksort(greater)

li = [49, 38, 65, 97, 76, 13, 27, 49]
# quicksort(li)
# quick_sort(li, 0, len(li) - 1)
# print(quicksort(li))


# 实现快速排序
def bubble_sort(li):
    unsorted_list_index = len(li)-1
    sorted = False
    while not sorted:
        sorted = True
        for i in range(unsorted_list_index):
            if li[i] > li[i+1]:
                sorted = False
                li[i], li[i+1] = li[i+1], li[i]
        unsorted_list_index = unsorted_list_index -1

li = [49, 38, 65, 97, 76, 13, 27, 49]
bubble_sort(li)
print(li)


# 斐波拉契数列
def fib():
    m = 0
    n = 1

    while True:
        m, n = n, m + n
        yield m

for a in fib():
    if a > 300:
        break
    print(a)


# 100 以内素数
num = []
for i in range(2, 100):
    j = 2
    for j in range(2, i):
        if (i % j == 0):
            break
    else:
        num.append(i)
print(num)

# yield 实现斐波拉契
def fab(max):
    n,a,b = 0,0,1
    while n<max:
        yield b
        a,b = b, a+b
        n+=1

for a in fab(5):
    print(a)

# yield 读取文件
def read_file(fpath): 
   BLOCK_SIZE = 1024 
   with open(fpath, 'rb') as f: 
       while True: 
           block = f.read(BLOCK_SIZE) 
           if block: 
               yield block 
           else: 
               return
