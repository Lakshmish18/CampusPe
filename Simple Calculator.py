""" Simple Calculator using Functions
 This program performs one calculation based on the selected  choice."""

# addition
def add(a, b):
    return a + b

# subtraction
def subtract(a, b):
    return a - b

# multiplication
def multiply(a, b):
    return a * b

# division
def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    else:
        return a / b


# main program
print("------ SIMPLE CALCULATOR ------")
print("1. Addition")
print("2. Subtraction")
print("3. Multiplication")
print("4. Division")

choice = input("Enter your choice from above (1-4): ")

try:
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    if choice == "1":
        result = add(num1, num2)
        print("Result:", result)

    elif choice == "2":
        result = subtract(num1, num2)
        print("Result:", result)

    elif choice == "3":
        result = multiply(num1, num2)
        print("Result:", result)

    elif choice == "4":
        result = divide(num1, num2)
        print("Result:", result)

    else:
        print("Invalid choice! Please select only  between 1 to 4.")

except ValueError:
    print("Invalid input! Please enter numbers only.")