class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.instance = add
 
    def __call__(self,*args):
        return self.instance(*args)
 
def add(args):
    return args[0] + args[1]
 
a = Person('p1', 20)
print(a([1,2]))


# 定义Role类
class Role:
    def __init__ (self, name):
        self.name = name
    # 定义__call__方法
    def __call__(self):
        print('执行Role对象')
r = Role('管理员')
# 直接调用Role对象，就是调用该对象的__call__方法, 如果没有__call__方法，'r()' 这种调用方式是错误的
r()  
