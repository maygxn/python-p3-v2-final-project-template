from models.__init__ import CURSOR, CONN
import datetime
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

    @classmethod
    def insert_order(cls, order_items, cost):
        sql = """
            INSERT INTO orders (date, order_items, cost)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (datetime.datetime.now(), str(order_items), cost))
        CONN.commit()