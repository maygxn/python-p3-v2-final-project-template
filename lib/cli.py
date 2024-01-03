# lib/cli.py
from menu_items import Menu
from helpers import (
    exit_program,
    helper_1
)
# create menu items
menu_items = [
    Menu(1, "Loaded Jalapeno Cheese Bytes", 10),
    Menu(2, "Baked Feta Bytes", 8),
    Menu(3, "Crab Cake Bytes",11),
    Menu(4, "Byte Smash Burger Combo",12),
    Menu(5, "Byte Smash Burger w/ Cheese Combo",13),
    Menu(6, "Spicy Chicken Sandwich Combo",11),
    Menu(7, "Chicken Tenders Combo",10),
    Menu(8, "Bacon Byte Burger Combo",14),
    Menu(9, "Southwest Salad",12),
    Menu(10, "Soft Drink",3),
    Menu(11, "Lemonade",3)
]

def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            order_food()
        elif choice == "2":
            print("helper func 2 - order food")
        elif choice == "3":
            print("helper func 3 - view order history")
        elif choice == "4":
            print("Reorder")
        else:
            print("Invalid choice")

def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. View Menu")
    print("2. Order Food")
    print("3. View all orders")
    print("4. Reorder")

def view_menu():
    print("Select Menu Item:")
    print("0 - Back to Main Menu")
    for item in menu_items:
        print(f"{item.item_number} - {item.name}: ${item.price}")
    
# def view_menu():
#     print("Select Menu Item:")
    
#     while True:
        
def order_food():
    while True:
        view_menu()
        choice = input("Enter item number to order (0 to finish):")
    
        if choice == "0":
            break
        elif not choice.isdigit():
            print("Invalid input.")
            continue
        elif choice == menu_items.item_number:
            print(menu_items)
            

if __name__ == "__main__":
    main()