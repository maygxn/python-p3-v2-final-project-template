import datetime
from models.__init__ import CURSOR, CONN
import sqlite3

class Orders:
    def __init__(self):
        self.conn = sqlite3.connect('company.db')
        self.cursor = self.conn.cursor()

    # ----- ORDER CONSTRAINTS------#
    @property
    def order_items(self):
        return self._order_items

    @order_items.setter
    def order_items(self, value):
        if value is None:
            raise ValueError("Menu item cannot be null.")
        self._order_items = value
    # ----- ORDER CONSTRAINTS------#

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
        self.cursor.execute("SELECT order_items, customer_id FROM orders WHERE id = ?", (order_number,))
        result = self.cursor.fetchone()
        return result if result else None

    @classmethod
    def create_table(cls):
        # **** !!!! COMMENT OUT to persist, Uncomment to delete existing table contents !!! ****
        CURSOR.execute("DROP TABLE IF EXISTS orders")
        CONN.commit()

        sql = """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                date DATE,
                order_items TEXT,
                cost INT,
                customer_id INTEGER,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """
        # print(f"Executing SQL: {sql}")  # Comment out or remove this line
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def insert_order(cls, order_items, cost, customer_id):
        sql = """
            INSERT INTO orders (date, order_items, cost, customer_id)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (datetime.datetime.now(), str(order_items), cost, customer_id))
        CONN.commit()

    @classmethod
    def update_order(cls, order_number, updated_order_items, total_cost):
        # Display the current order for confirmation
        print("Updated Order:")
        print(f"Order Number: {order_number}, Updated Order Items: {updated_order_items}, Updated Cost: {total_cost}")

        # Update the order in the database
        sql = """
            UPDATE orders
            SET order_items = ?, cost = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (str(updated_order_items), total_cost, order_number))
        CONN.commit()
        print("Order updated successfully.")
        # # Update the order in the database
        # sql = """
        #     UPDATE orders
        #     SET order_items = ?, cost = ?
        #     WHERE id = ?
        # """
        # self.cursor.execute(sql, (str(updated_order_items), total_cost, order_number))
        # self.conn.commit()
        # print("Order updated successfully.")

def update_final_order(order_number, updated_order_items):
    total_cost = sum(item.price for item in updated_order_items)
    order_item_names = [item.name for item in updated_order_items]

    # Display the updated order for confirmation
    print("Updated Order:")
    print(f"Order Number: {order_number}, Updated Order Items: {order_item_names}, Updated Cost: ${total_cost}")

    # Update the order in the database
    sql = """
        UPDATE orders
        SET order_items = ?, cost = ?
        WHERE id = ?
    """
    CURSOR.execute(sql, (', '.join(order_item_names), total_cost, order_number))
    CONN.commit()
    print("Order updated successfully.")

    return updated_order_items

