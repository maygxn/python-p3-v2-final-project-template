# lib/cli.py
from menu_items import Menu
from helpers import (
    exit_program,
    helper_1
)
# create menu items
menu_items = [
    Menu("Loaded Jalapeno Cheese Bytes", 10),
    Menu("Baked Feta Bytes", 8),
    Menu("Crab Cake Bytes",11),
    Menu("Byte Smash Burger Combo",12),
    Menu("Byte Smash Burger w/ Cheese Combo",13),
    Menu("Spicy Chicken Sandwich Combo",11),
    Menu("Chicken Tenders Combo",10),
    Menu("Bacon Byte Burger Combo",14),
    Menu("Southwest Salad",12),
    Menu("Soft Drink",3),
    Menu("Lemonade",3)
]

def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            view_menu()
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
    print("Menu:")
    for item in menu_items:
        print(f"{item.name}: ${item.price}")

if __name__ == "__main__":
    main()