# Number Pyramid Pattern
"""1. This program prints a centered number pyramidlike below .
   1
  1 2
 1 2 3
1 2 3 4
"""

total_rows = int(input("Enter number of rows: "))

# Outer loop controls the number of rows
for current_row in range(1, total_rows + 1):
    
    # Print spaces for pyramid structure
    for space in range(total_rows - current_row):
        print(" ", end="")
    
    # Print numbers for the current row
    for number in range(1, current_row + 1):
        print(number, end=" ")
    
    # Move to next line
    print()

"""2. Reverse Number Triangle Pattern
 This program prints numbers in decreasing rows.
1 2 3 4
1 2 3
1 2
1
"""
total_rows = int(input("Enter number of rows: "))

# Outer loop controls rows (decreasing order)
for current_row in range(total_rows, 0, -1):
    
    # Inner loop prints numbers from 1 to current_row
    for number in range(1, current_row + 1):
        print(number, end=" ")
    
    # Move to next line after each row
    print()