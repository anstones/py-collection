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
