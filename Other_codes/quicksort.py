import time
def timewapper(func):
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        timediff = time.time() - start
        print(timediff)
        return result
    return inner

@timewapper
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

        while left < right and li[left] < mid:
            left += 1
        li[right] = li[left]

    li[left] = mid
    quick_sort(li, start, left-1)
    quick_sort(li, left+1, end)

@timewapper
def quick_sort_1(li):
    less = []
    greater = []
    if len(li) <= 1:
        return li
    privot = li.pop()
    for x in li:
        if x <= privot:
            less.append(x)
        else:
            greater.append(x)

    return quick_sort_1(less) + [privot] + quick_sort_1(greater)

li = [49, 38, 65, 97, 76, 13, 27, 49]
quick_sort(li, 0, len(li)-1)
print(li)
print(quick_sort_1(li))
