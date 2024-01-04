from models.__init__ import CURSOR, CONN
import sqlite3

class Users:
    def __init__(self, name, email, delivery_address):
        self.name = name
        self.email = email 
        self.delivery_address = delivery_address

    @classmethod
    def create_customer_table(cls):
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
Users.insert_customer('Tyler','tyler@tyler.com','123 Tyler St')
Users.insert_customer('Meagan','meagan@meagan.com','123 Meagan St')
Users.insert_customer('Jenny','jenny@jenny.com','123 Jenny St')