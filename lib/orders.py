from models.__init__ import CURSOR, CONN

class Orders:
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)
    
    def get_order_history(self):
        return self.orders
    
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            date DATE,
            order_items TEXT,
            cost INT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()