#Factorial Program
def fact(n): 
    return 1 if n == 0 else n * fact(n - 1)
n = int(input("Enter a non-negative integer: "))
print("Factorial:", fact(n) if n >= 0 else "Not defined for negative numbers")