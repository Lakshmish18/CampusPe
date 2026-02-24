""" Age Calculator Program 
This program calculates age using only basic Python."""

# Taking current year from the user
current_year = int(input("Enter current year: "))

# Taking birth year from the user
birth_year = int(input("Enter your birth year: "))

# Checking if input entered  is valid or not 
if birth_year > current_year:
    print("Invalid input! Birth year can't be greater than current year.")
elif birth_year <= 0:
    print("Please enter a valid birth year.")
else:
    age = current_year - birth_year
    print("Your age is:", age, "years")