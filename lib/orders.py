class Orders:
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)
    
    def get_order_history(self):
        return self.orders