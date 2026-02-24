# Number System Converter
# This program converts numbers between different number systems.

# Decimal to Binary
def decimal_to_binary(number):
    return bin(number) 

# Decimal to Octal
def decimal_to_octal(number):
    return oct(number)  

# Decimal to Hexadecimal
def decimal_to_hexadecimal(number):
    return hex(number)   

# Binary to Decimal
def binary_to_decimal(binary_number):
    return int(binary_number, 2)


print("---- Number System Converter ----")

while True:
    print("\n1. Decimal to Binary\n")
    print("2. Decimal to Octal")
    print("3. Decimal to Hexadecimal")
    print("4. Binary to Decimal")
    print("5. Exit\n")

    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        number = int(input("Enter decimal number: "))
        print("Binary:", decimal_to_binary(number))

    elif choice == "2":
        number = int(input("Enter decimal number: "))
        print("Octal:", decimal_to_octal(number))

    elif choice == "3":
        number = int(input("Enter decimal number: "))
        print("Hexadecimal:", decimal_to_hexadecimal(number))

    elif choice == "4":
        binary_number = input("Enter binary number: ")
        print("Decimal:", binary_to_decimal(binary_number))

    elif choice == "5":
        print("Program Ended.")
        break

    else:
        print("Invalid choice.")