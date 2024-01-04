from models.__init__ import CURSOR, CONN
import sqlite3

class Users:
    def __init__(self, name, email, delivery_address):
        self.name = name
        self.email = email 
        self.delivery_address = delivery_address

    @classmethod
    def create_customer_table(cls):
        # **** !!!! COMMENT OUT to persist, Uncomment to delete existing table contents !!! ****
        # CURSOR.execute("DROP TABLE IF EXISTS customers")
        # CONN.commit()
        sql = """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                delivery_address TEXT NOT NULL
            )
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def insert_customer(cls, name, email, delivery_address):
        sql = """
            INSERT INTO customers (name, email, delivery_address) VALUES (?,?,?)
        """
        CURSOR.execute(sql, (name, email, delivery_address))
        CONN.commit()


Users.create_customer_table()