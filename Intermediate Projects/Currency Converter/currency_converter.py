import sys

def print_menu():
    print()
    print("Welcome to the Currency Converter!")
    print()
    print("Which action would you like to perform?")

print_menu()

def input_currency():
    currency_to_convert = input()
    currency_dict[currency_to_convert]