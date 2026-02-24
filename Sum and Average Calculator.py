# Sum and Average Calculator
try:
    # here split() helps to  separates input, map(float, ...) helps to convert each string value entered into  float number, list() stores them for to calculate  sum() and len()
    numbers = list(map(float, input("Enter numbers separated by space: ").split()))
    total_sum = sum(numbers)
    average_value = total_sum / len(numbers)
    print("Sum:", total_sum)
    print("Average:", average_value)
except (ValueError, ZeroDivisionError):
    print("Invalid input! Please enter valid numbers.")