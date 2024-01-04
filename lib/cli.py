# lib/cli.py
from models.__init__ import CURSOR, CONN
from users import Users
from menu_items import Menu
from orders import Orders
from helpers import (
    exit_program,
    helper_1
)
current_order = []
# create menu items
menu_items = [
    Menu(1, "Loaded Jalapeno Cheese Bytes", 10),
    Menu(2, "Baked Feta Bytes", 8),
    Menu(3, "Crab Cake Bytes", 11),
    Menu(4, "Byte Smash Burger Combo", 12),
    Menu(5, "Byte Smash Burger w/ Cheese Combo", 13),
    Menu(6, "Spicy Chicken Sandwich Combo", 11),
    Menu(7, "Chicken Tenders Combo", 10),
    Menu(8, "Bacon Byte Burger Combo", 14),
    Menu(9, "Southwest Salad", 12),
    Menu(10, "Soft Drink", 3),
    Menu(11, "Lemonade", 3)
]

def main():
    Orders.create_table()
    order_history = Orders()

    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            order_food()
        elif choice == "2":
            display_order_history(order_history)
        elif choice == "3":
            reorder(order_history)
        elif choice == "4":
            delete_order(order_history)
        else:
            print("Invalid choice")

def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. View Menu")
    print("2. View all orders")
    print("3. Reorder")
    print("4. Delete an order")

def view_menu():
    print("Select Menu Item:")
    print("0 - Back to Main Menu")
    for item in menu_items:
        print(f"{item.item_number} - {item.name}: ${item.price}")
    print("98 - Remove an item from cart")
    print("99 - View Cart")

def view_cart(current_order):
    print("Your current order contains: ")
    total_price = 0
    for item in current_order:
        print(f"{item.name} -- ${item.price}")
        total_price += item.price
    print(f"Total is ****${total_price}****")
    while True:
        choice = input("Press '000' to complete order or any other key to continue ordering:")
        if choice == "000":
            customer_id = get_or_create_customer()
            Orders.insert_order([item.name for item in current_order], total_price, customer_id)
            print("Your order has been successfully placed!")
            current_order.clear()
            return True
        else:
            view_menu()
            return False

def remove_item(current_order):
    view_cart(current_order)
    print("Enter the name of the item you want to remove:")
    item_name = input("> ")
    for item in current_order:
        if item.name == item_name:
            current_order.remove(item)
            print(f"You have successfully removed {item.name} from your cart.")
            view_cart(current_order)
            return
    print("Item not found in cart.")

def get_or_create_customer():
    print("Enter your email:")
    email = input("> ")
    CURSOR.execute("SELECT id FROM customers WHERE email = ?", (email,))
    customer = CURSOR.fetchone()
    if customer:
        return customer[0]
    else:
        print("Enter your name:")
        name = input("> ")
        print("Enter your delivery address:")
        address = input("> ")
        Users.insert_customer(name, email, address)
        return CURSOR.lastrowid

def order_food():
    global current_order
    customer_id = get_or_create_customer()
    while True:
        view_menu()
        choice = input("Enter item number to order (Enter 99 to view cart and to confirm order):")
    
        if choice == "0":
            break
        elif not choice.isdigit():
            print("Invalid input.")
            continue
        elif choice == "98":
            remove_item(current_order)
        elif choice == "99":
            if view_cart(current_order):
                current_order.clear()
                break
            
        else:
            for item in menu_items:
                if item.item_number == int(choice):
                    current_order.append(item)
                    print(f"You have successfully added {item.name} to your cart.")

def display_order_history(order_history):
    history = order_history.get_order_history()
    if history:
        for order in history:
            print(f"Order Number: {order[0]}, Order Date: {order[1]}, Order Items: {order[2]}, Cost: {order[3]}")
    else:
        print("No orders have been placed.")

def delete_order(order_history):
    display_order_history(order_history)
    print("Enter the order number you want to delete:")
    order_number = input("> ")
    if order_number.isdigit():
        order_number = int(order_number)
        if order_history.delete_order(order_number):
            print(f"You have successfully deleted order number {order_number}.")
        else:
            print("Order not found.")
    else:
        print("Invalid input. Please enter a valid order number.")

def reorder(order_history):
    # need this here to display past orders
    display_order_history(order_history)
    print("Enter the order number you wish to reorder:")
    order_number = input("> ")
    if order_number.isdigit():
        order_number = int(order_number)
        order_items_str = order_history.get_specific_order(order_number)
        if order_items_str:
            # converting string back to a list
            order_items = eval(order_items_str)
            total_cost = sum(item.price for item in menu_items if item.name in order_items)
            print(f"Reordering items: {order_items}, Total Cost: ${total_cost}")
            Orders.insert_order(order_items, total_cost)
            print("Your reorder has been successfully placed!")
        else:
            print("Order not found.")
    else:
        print("Invalid input. Please enter a valid order number.")

if __name__ == "__main__":
    main()
