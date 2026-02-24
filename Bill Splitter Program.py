# Simple Bill Splitter Program
# This program divides the total bill equally among people.

#function to fetch total bill amount

def get_total_bill_amount():
    while True:
        try:
            total_bill_amount = float(input("Enter total bill amount: ₹ "))
            
            # bill cannot be negative
            if total_bill_amount < 0:
                print("Bill amount cannot be negative. Try again.")
                continue
            
            return total_bill_amount
        
        except ValueError:
            print("Invalid input! Please enter a valid number.")

# function to fetch number of people
def get_number_of_people():
    while True:
        try:
            number_of_people = int(input("Enter number of people: "))
            
            # people must be greater than 0
            if number_of_people <= 0:
                print("Number of people must be greater than 0. Try again.")
                continue
            
            return number_of_people
        
        except ValueError:
            print("Invalid input! Please enter a whole number.")


# function to calculate each person's share
def calculate_individual_share(total_bill_amount, number_of_people):
    return total_bill_amount / number_of_people


# Main function
def main():
    print("------ Bill Splitter ------\n")
    
    total_bill_amount = get_total_bill_amount()
    number_of_people = get_number_of_people()
    
    individual_share = calculate_individual_share(
        total_bill_amount, number_of_people
    )
    
    print("\nEach person should pay: Rs", round(individual_share, 2))


main()