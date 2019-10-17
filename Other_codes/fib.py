from collections import Iterator

# 计算前n个fib数列
def fib(n):
    a,b = 1,1
    while n>0:
        n-=1
        yield a
        a,b = b, a+b

for i in fib(10):
    print(i)

# 计算max之前的fib数列
def fib_max(max):
    a,b = 1,1
    while a <= max:
        yield a
        a,b = b,a+b

for i in fib_max(57):
    print(i)

# 迭代器实现fib
class Fib():
    def __init__(self, n):
        self.a = 1
        self.b = 1
        self.n = n

    def __iter__(self):
        return self

    def __next__(self):
        if self.n > 0:
            self.n -= 1
            value = self.a
            self.a,self.b = self.b, self.a+self.b
            return value

        else:
            raise StopIteration()

print(isinstance(Fib(10), Iterator))
