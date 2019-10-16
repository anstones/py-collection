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

