# codeing=utf-8
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


# li = [49, 38, 65, 97, 76, 13, 27, 49]
# quick_sort(li, 0, len(li) - 1)
# print(li)


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

num = []
for i in range(2, 100):
    j = 2
    for j in range(2, i):
        if (i % j == 0):
            break
    else:
        num.append(i)
print(num)




