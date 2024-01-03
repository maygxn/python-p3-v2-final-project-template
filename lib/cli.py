# lib/cli.py

from helpers import (
    exit_program,
    helper_1
)


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            helper_1()
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

if __name__ == "__main__":
    main()