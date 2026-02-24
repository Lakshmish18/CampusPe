# Multiplication Table Generator
# Prints multiplication table for a given number.

def print_table(number):
    """Prints table from 1 to 10 for the given number."""
    for multiplier in range(1, 11):  # 10 iterations
        print(f"{number} x {multiplier} = {number * multiplier}")

try:
    number = int(input("Enter a number: "))  # User input
    
    print_table(number)

except ValueError:
    # handles invalid (noninteger) input
    print("Invalid input! Please enter a valid integer.")