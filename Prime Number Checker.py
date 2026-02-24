#Prime Number Checker 

def is_prime(number):
    if number <= 1: return False  # 0,1,negatives not prime
    for divisor in range(2, int(number**0.5) + 1):  # checks till  sqare root of n
        if number % divisor == 0: return False
    return True

try:
    input_number = int(input("Enter an integer: "))
    print("Prime Number" if is_prime(input_number) else "Not a Prime Number")
except ValueError:
    print("Invalid input! Please enter a valid integer.")