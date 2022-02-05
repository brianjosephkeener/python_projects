class Store:
    def __init__(self, name):
        self.name = name
        self.products = []
    
    def add_product(self, new_product):
        self.products.append(new_product)

    def sell_product(self, id):
        print(f"selling {self.products[id]}")
        self.products.pop(id)
    
class Product:
    def __init__(self, name, price, category):
        self.price = price
        self.category = category
        self.name = name
    
    def update_price(self, percent_change, is_increased):
        if is_increased == True:
            increase = self.price * percent_change
            self.price = self.price + increase
            return self.price
        if is_increased == False: 
            decrease = self.price * percent_change
            self.price = self.price - decrease
            return self.price

    def print_info(self):
        print(self.name, self.price, self.category)

Mystore = Store("Walmart")



p1 = Product("Shaving Cream", 1.99, "Adult")
p2 = Product("Chris Brown", 69, "Adult Child")
p3 = Product("Earring", .99, "Child")

Mystore.add_product(p1)
Mystore.add_product(p2)
Mystore.add_product(p3)

print(Mystore.products)
Mystore.sell_product(2)
print(Mystore.products)