# Leap Year Checker Program
# This program checks whether a given year is a leap year or not.
# using standard leap year rules.

# Function to check leap year
def is_leap_year(year):
    """
    Returns True if the year is a leap year,otherwise returns False. """

    # Leap year rules:
    # the year should be divisible by 4
    # Should not be divisible by 100 unless divisible by 400
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else:
        return False
# Main function
def main():
    try:
        # Taking input from user
        input_year = int(input("Enter a year: "))

        # Edge case: Year should be positive
        if input_year <= 0:
            print("Please enter a valid positive year.")
            return

        # Calling function
        if is_leap_year(input_year):
            print(input_year, "is a Leap Year.")
        else:
            print(input_year, "is NOT a Leap Year.")

    except ValueError:
        print("Invalid input! Please enter a valid integer year.")


# Run the program
main()