from models.__init__ import CURSOR, CONN
import datetime
import sqlite3
class Orders:
    def __init__(self):
        self.orders = []
        self.conn = sqlite3.connect('company.db')
        self.cursor = self.conn.cursor()

    def add_order(self, order):
        self.orders.append(order)
    
    def get_order_history(self):
        self.cursor.execute("SELECT * FROM orders")
        return self.cursor.fetchall()
    
    def delete_order(self, order_number):
        # need this here to display list of previous orders
        print("Here are your current orders:")
        orders = self.get_order_history()
        for order in orders:
            print(f"Order Number: {order[0]}, Order Items: {order[2]}, Cost: {order[3]}")
        # deletion
        self.cursor.execute("DELETE FROM orders WHERE id = ?", (order_number,))
        self.conn.commit()
        print(f"Order number {order_number} has been deleted.")
    
    def get_specific_order(self, order_number):
        self.cursor.execute("SELECT order_items FROM orders WHERE id = ?", (order_number,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
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