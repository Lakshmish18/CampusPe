# Ticket Pricing System
# This program calculates ticket price based on age category.It handles invalid input and edge cases using try-except.


# Function to calculate ticket price based on age
def calculate_ticket_price(customer_age):
    """
    Returns ticket price based on given age.
    Pricing:
    - Below 5 years: Free
    - 5 to 17 years: ₹100
    - 18 to 59 years: ₹200
    - 60 and above: ₹150
    """

    if customer_age < 5:
        return 0
    elif 5 <= customer_age <= 17:
        return 100
    elif 18 <= customer_age <= 59:
        return 200
    else:
        return 150


# Main function
def main():
    try:
        #user input
        age_input = int(input("Enter your age: "))

        #Age should be positive
        if age_input < 0:
            print("Age cannot be negative. Please enter a valid age.")
            return

        #Calculating price
        ticket_price = calculate_ticket_price(age_input)

        #Displaying result
        if ticket_price == 0:
            print("Ticket is FREE for children under 5.")
        else:
            print("Your ticket price is: ₹", ticket_price)

    except ValueError:
        print("Invalid input! Please enter a valid whole number for age.")


# Run program
main()