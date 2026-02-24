# Calculator Program
# basic arithmetic operations using each separate functions.

def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b): return "Division by zero not allowed" if b == 0 else a / b

def perform_operation(operation_function):
    first_number = float(input("Enter first number: "))
    second_number = float(input("Enter second number: "))
    print("Result:", operation_function(first_number, second_number))


print("\n---- Simple Calculator ----\n")

while True:
    print("\n1.Add  2.Subtract  3.Multiply  4.Divide  5.Exit\n")
    user_choice = input("Choose (1-5): ")

    if user_choice == "1":
        perform_operation(add)
    elif user_choice == "2":
        perform_operation(subtract)
    elif user_choice == "3":
        perform_operation(multiply)
    elif user_choice == "4":
        perform_operation(divide)
    elif user_choice == "5":
        print("Calculator Closed.")
        break
    else:
        print("Invalid choice.")