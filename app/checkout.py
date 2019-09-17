class Checkout(self, regular_price, category_name, quantity):
    def __init__(self):
        self.category_name = category_name
        self.regular_price = regular_price
        self.quantity = quantity
    
    @staticmethod
    def total_pricing(self):
        return self.regular_price * quantity
    
    # TODO: create dic for the pricing
    # TODO: Error handling
    @staticmethod
    def category_pricing(self, category):
        pricing = ['fiction': 1.5, 'regular': 3, 'novels': 1.5], 
        for key,value in pricing:
            if key == self.category_name:
                return value

    @classmethod
    def manage_order(clas):
        pass
