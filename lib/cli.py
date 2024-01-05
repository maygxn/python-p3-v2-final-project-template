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


def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. View Menu")
    print("2. View all orders")
    print("3. Reorder")
    print("4. Delete an order")
    print ("5. Update placed order")

def view_menu():
    print("Select Menu Item:")
    print("0 - Back to Main Menu")
    for item in menu_items:
        print(f"{item.item_number} - {item.name}: ${item.price}")
    print("98 - Remove an item from cart")
    print("99 - View Cart")

def view_cart(current_order):
    print("Your current order contains:")
    total_price = 0
    for item in current_order:
        print(f"{item.name} -- ${item.price}")
        total_price += item.price
    print(f"Total is ****${total_price}****")

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
    print("Enter the name of the item you want to remove (Enter '0' to go back):")
    item_name = input("> ").lower()

    if item_name == '0':
        return

    for i, item in enumerate(current_order):
        if item.name.lower() == item_name:
            removed_item = current_order.pop(i)
            print(f"You have successfully removed {removed_item.name} from your cart.")
            break
    else:
        print(f"No {item_name.capitalize()} found in cart.")

    return current_order

def view_cart(current_order):
    print("Your current order contains:")
    total_price = 0
    for item in current_order:
        print(f"{item.name} -- ${item.price}")
        total_price += item.price
    print(f"Total is ****${total_price}****")

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
            current_order = remove_item(current_order)
        elif choice == "99":
            view_cart(current_order)
            current_order = confirm_order(current_order, customer_id)
        else:
            for item in menu_items:
                if item.item_number == int(choice):
                    current_order.append(item)
                    print(f"You have successfully added {item.name} to your cart.")

def confirm_order(current_order, customer_id):
    view_cart(current_order)
    print("Enter '000' to complete order, or any other key to continue ordering:")
    choice = input("> ")
    
    if choice == "000":
        Orders.insert_order([item.name for item in current_order], sum(item.price for item in current_order), customer_id)
        print("Your order has been successfully placed!")
        current_order = []  # Clear the current order
        return current_order
    else:
        return current_order

def confirm_order(current_order, customer_id):
    view_cart(current_order)
    print("Enter '000' to complete order, or any other key to continue ordering:")
    choice = input("> ")
    
    if choice == "000":
        Orders.insert_order([item.name for item in current_order], sum(item.price for item in current_order), customer_id)
        print("Your order has been successfully placed!")
        current_order = []  # Clear the current order
        return current_order
    else:
        return current_order


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
        order_details = order_history.get_specific_order(order_number)
        print(order_details)    
        if order_details:
            order_items, customer_id = order_details
            total_cost = sum(item.price for item in menu_items if item.name in order_items)
            print(f"Reordering items: {order_items}, Total Cost: ${total_cost}")
            Orders.insert_order(order_items, total_cost, customer_id)
            print("Your reorder has been successfully placed!")
        else:
            print("Order not found.")
    else:
        print("Invalid input. Please enter a valid order number.")

# def update_order(order_history):
#     order_number = int(input("Order number to update: "))
#     new_items = input("Enter new items, comma-separated: ").split(', ')
#     total_cost = sum(Menu.get_price(item) for item in new_items)  # Ensure Menu.get_price() is implemented
#     order_history.update_order(order_number, new_items, total_cost)
#     print(f"Order {order_number} updated.")



# def update_order(order_history):
#     display_order_history(order_history)
#     print("Enter the order number you want to update:")
#     order_number = input("> ")

#     if order_number.isdigit():
#         order_number = int(order_number)
#         order_details = order_history.get_specific_order(order_number)

#         if order_details:
#             print(f"Order Number: {order_details[0]}, Order Date: {order_details[1]}, Order Items: {order_details[2]}, Cost: {order_details[3]}")
#             current_order = order_details[2][:]  # Create a copy to avoid modifying the original list
            
#             while True:
#                 print("1. Add item to order")
#                 print("2. Remove item from order")
#                 print("3. Finish updating order")
#                 choice = input("> ").lower()

#                 if choice == "1":
#                     current_order = add_item_to_order(current_order)
#                 elif choice == "2":
#                     current_order = remove_item_from_order(current_order)
#                 elif choice == "3":
#                     update_final_order(order_number, current_order)
#                     break
#                 else:
#                     print("Invalid choice. Please enter a valid option.")
#         else:
#             print("Order not found.")
#     else:
#         print("Invalid input. Please enter a valid order number.")

def update_order(order_history):
    display_order_history(order_history)
    print("Enter the order number you want to update (Enter '0' to go back):")
    order_number = input("> ")

    if order_number == '0':
        return

    if order_number.isdigit():
        order_number = int(order_number)
        order_details = order_history.get_specific_order(order_number)

        if order_details and len(order_details) == 2:
            order_items, customer_id = order_details
            total_cost = sum(item.price for item in menu_items if item.name in order_items)
            print(f"Updating items: {order_items}, Total Cost: ${total_cost}")
            current_order = [item for item in menu_items if item.name in order_items]  # Convert order_items to Menu objects

            while True:
                print("1. Add item to order")
                print("2. Remove item from order")
                print("3. Finish updating order")
                choice = input("> ").lower()

                if choice == "1":
                    current_order = add_item_to_order(current_order)
                elif choice == "2":
                    current_order = remove_item_from_order(current_order)
                elif choice == "3":
                    current_order = update_final_order(order_number, current_order)
                    print("Your order has been successfully updated!")
                    break
                else:
                    print("Invalid choice. Please enter a valid option.")
        else:
            print("Order not found or incomplete order details.")
    else:
        print("Invalid input. Please enter a valid order number.")

def add_item_to_order(existing_order_items):
    while True:
        view_menu()
        print("Enter item number to add to the order (Enter 99 to view current order):")
        choice = input("> ")

        if choice == "99":
            view_cart(existing_order_items)
            continue

        if choice.isdigit():
            choice = int(choice)
            selected_item = next((item for item in menu_items if item.item_number == choice), None)
            if selected_item:
                existing_order_items.append(selected_item)
                print(f"You have successfully added {selected_item.name} to the order.")
                view_cart(existing_order_items)  # Show the updated order
            else:
                print("Invalid choice. Item not added to the order.")
        else:
            print("Invalid input. Please enter a valid item number or '99' to view the current order.")

        another_item = input("Add another item? (yes/no): ").lower()
        if another_item != "yes":
            break

    return existing_order_items

def remove_item_from_order(existing_order_items):
    while True:
        view_cart(existing_order_items)
        print("Enter the name of the item you want to remove (Enter '0' to go back):")
        item_name = input("> ").lower()

        if item_name == '0':
            break

        if any(item.name.lower() == item_name for item in existing_order_items):
            existing_order_items = [item for item in existing_order_items if item.name.lower() != item_name]
            print(f"You have successfully removed {item_name} from the order.")
            view_cart(existing_order_items)  # Show the updated order
        else:
            print(f"No {item_name.capitalize()} found in the order.")

        another_item = input("Remove another item? (yes/no): ").lower()
        if another_item != "yes":
            break

    return existing_order_items

def update_final_order(order_number, updated_order_items):
    total_cost = sum(item.price for item in menu_items if item.name in updated_order_items)
    Orders.update_order(order_number, updated_order_items, total_cost)
    print("Order updated successfully.")


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
        elif choice == "5":  
            update_order(order_history)
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
