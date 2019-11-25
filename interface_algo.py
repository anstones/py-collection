def binry_search(lists, item):
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


def binry_search(num,l,start=None,end=None):
	""" 二分法查找:递归 """
	start = start if start else 0
	end = end if end is None else len(l) - 1
	mid = (end + start) // 2
	if start > end:
		return None
	elif l[mid] > num :
		return binry_search(num, l, start, mid-1)
	elif l[mid] < num:
		return binry_search(num, l, mid+1, end)
	elif l[mid] == num:
		return mid
        

def Singleton():
	""" 单例模式 """
	def __init__(self):
		pass
		
		
	def __new__(cls, *args, **kwargs):
		if not hasattr(Singleton, "_instance"):
			Singleton._instance = object.__new__(cls, *args, **kwargs)
		return Singleton._instance
		
		

def func(n):
	""" 斐波拉契数列 """
	a,b = 0,1
	while n >0:
		a,b = b, a+b
		n -= 1
		yield a
	

def mp_sort(li):
	""" 冒泡排序 """
    for i in range(len(li)):
        for j in range(len(li)-i-1):
            if li[j] > li[j+1]:
                li[j+1], li[j]= li[j], li[j+1]
            else:
                pass
    return li
		
		


def quick_sort(li, start, end):
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
	quick_sort(li, start, left-1)
	quick_sort(li, left+1, end)
	

def addBinary(self, a, b):
        """ 二进制运算 """
        a = int(a,2)
        b = int(b,2)
        return bin(a+b)[2:]
		
		

def fun():
	""" 有一组“+”和“-”符号，要求将“+”排到左边，“-”排到右边，写出具体的实现方法。 """
	l=['-', '+', '-', '+', '+', '-']
	a = []
	b = []
	for i in range(len(l)):
		if l[i] == '+':
			a.append(l[i])
		else:
			b.append(l[i])
	return a+b
	

class Node(object):
	""" 单链表反转python实现 """
    def __init__(self, data, next=None):
        self.val = data
        self.next = next
 
def fun4(head):
    if head == None:
        return None
    L,M,R = None,None,head
    while R.next != None:
        L = M
        M = R
        R = R.next
        M.next = L
    R.next = M
    return R
#测试用例
if __name__ == '__main__':
    l1 = Node(3)
    l1.next = Node(2)
    l1.next.next = Node(1)
    l1.next.next.next = Node(9)
    l = fun4(l1)
    print (l.val, l.next.val, l.next.next.val, l.next.next.next.val)
	
	

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
		

def node(l1, l2):
	""" 交叉链表求交点 """
    length1, length2 = 0, 0
    # 求两个链表长度
    while l1.next:
        l1 = l1.next#尾节点
        length1 += 1
    while l2.next:
        l2 = l2.next#尾节点
        length2 += 1

    #如果相交
    if l1.next == l2.next:
        # 长的链表先走
        if length1 > length2:
            for _ in range(length1 - length2):
                l1 = l1.next
            return l1#返回交点
        else:
            for _ in range(length2 - length1):
                l2 = l2.next
            return l2#返回交点
    # 如果不相交
    else:
        return
		
		
class MyStack(object):
	""" 用列表模拟栈，和相关栈操作 """
 
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.queue = []
        
 
    def push(self, x):
        """
        Push element x onto stack.
        :type x: int
        :rtype: void
        """
        self.queue.append(x)
 
    def pop(self):
        """
        Removes the element on top of the stack and returns that element.
        :rtype: int
        """
        if len(self.queue)!=0:
            temp = self.queue[-1]
            del self.queue[-1]
            return temp
        else:
            return False
 
    def top(self):
        """
        Get the top element.
        :rtype: int
        """
        if len(self.queue)!=0:
            return self.queue[-1]
        else:
            return False
 
    def empty(self):
        """
        Returns whether the stack is empty.
        :rtype: bool
        """
        if len(self.queue)==0:
            return True
        else:
            return False
			
			
'''
题目描述
如何得到一个数据流中的中位数？如果从数据流中读出奇数个数值，
那么中位数就是所有数值排序之后位于中间的数值。如果从数据流中读出偶数个数值，
那么中位数就是所有数值排序之后中间两个数的平均值。
我们使用Insert()方法读取数据流，使用GetMedian()方法获取当前读取数据的中位数。
使用插入排序算法
'''

class Solution:
    def __init__(self):
        self.sorted=[]
    def Insert(self, num):
        # write code here
        if len(self.sorted)==0:
            self.sorted.append(num)
        else:
            for i in range(len(self.sorted)):
                if self.sorted[i]>num:
                    self.sorted=self.sorted[:i]+[num]+self.sorted[i:]
                    return
            self.sorted.append(num)
            # 如果遍历完了当前排序好的数组，都没有找到比当前数据流中新加入的元素num数值更大的元素
            # 说明num应该被添加在列表最后
    def GetMedian(self,n=None):
        # write code here
        pos=len(self.sorted)//2
        if len(self.sorted)%2==0:
            return (self.sorted[pos-1]+self.sorted[pos]+0.0)/2
        else:
            return self.sorted[pos]+0.0
if __name__=='__main__':
    a=Solution()
    inp=[5, 2, 3, 4, 1, 6, 7, 0, 8]
    for num in inp:
        a.Insert(num)
        print(a.GetMedian())
    # "5.00 3.50 3.00 3.50 3.00 3.50 4.00 3.50 4.00
	
	
class Solution(object):
	""" 二叉搜索树中第 K 小的元素 """
    def kthSmallest(self, root, k):
        """
        :type root: TreeNode
        :type k: int
        :rtype: int
        """
        def inorderTraversal(root):
            if root is None:
                return []
            res = []
            res.extend(inorderTraversal(root.left))
            res.append(root.val)
            res.extend(inorderTraversal(root.right))
            return res
        return inorderTraversal(root)[k - 1]
