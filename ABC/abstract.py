from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')


class LineItem:
    '''购物车条目类 每个条目有属性：产品 价格 数量'''

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        '''购物车一个条目的总价'''
        return self.price * self.quantity


class Order:
    '''订单类 客户 购物车 折扣 计算总价和应付款 '''

    def __init__(self, customer, cart, promotion):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        '''打折前的总价'''
        # if not hasattr(self, '__total'): # 为什么要加这句判断？
        #     self.__total = sum(item.total() for item in self.cart)
        # return self.__total
        return sum(item.total() for item in self.cart)

    def due(self):
        '''打折后的应付款'''
        if not self.promotion:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())



def fidelity_promo(order):
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0

def bulk_item_promo(order):
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount

def large_order_promo(order):
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0

# 计算那种打折方案
promos = [fidelity_promo, bulk_item_promo, large_order_promo]

def best_promo(order):
    return max(promo(order) for promo in promos) # 生成器表达式 简洁有力！

joe = Customer('John Doe', 0)
ann = Customer('Ann Smith', 1100)
cart = [LineItem('banana', 4, .5), 
        LineItem('apple', 10, 1.5), 
        LineItem('watermellon', 5, 5.0)]
print(Order(joe, cart, fidelity_promo))
print(Order(ann, cart, fidelity_promo))
banana_cart = [LineItem('banana', 30, .5), 
                LineItem('apple', 10, 1.5)]
print(Order(joe, banana_cart, bulk_item_promo))
long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
print(Order(joe, long_order, large_order_promo))
print(Order(joe, cart, large_order_promo))
