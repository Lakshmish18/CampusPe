# Simple ATM Simulator
""" This program simulates basic ATM operations:
         Check Balance, Deposit Money, Withdraw Money, Exit"""
# It handles invalid input and edge cases safely.


# Function to display ATM menu
def display_menu():
    print("\n------ ATM MENU ------\n")
    print("1. Check Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Exit")


# Function to deposit money
def deposit(current_balance):
    try:
        deposit_amount = float(input("Enter amount to deposit: ₹ "))

        if deposit_amount <= 0:
            print("Deposit amount must be greater than 0.")
            return current_balance

        current_balance += deposit_amount
        print("Amount deposited successfully.")
        return current_balance

    except ValueError:
        print("Invalid input! Please enter a valid number.")
        return current_balance


# Function to withdraw money
def withdraw(current_balance):
    try:
        withdraw_amount = float(input("Enter amount to withdraw: ₹ "))

        if withdraw_amount <= 0:
            print("Withdrawal amount must be greater than 0.")
            return current_balance

        if withdraw_amount > current_balance:
            print("Insufficient balance!")
            return current_balance

        current_balance -= withdraw_amount
        print("Amount withdrawn successfully.")
        return current_balance

    except ValueError:
        print("Invalid input!! Please enter a valid number.")
        return current_balance


# Main function
def main():
    account_balance = 1000.0  # Initial balance

    print("Welcome to Simple ATM Simulator")

    while True:
        display_menu()

        try:
            user_choice = int(input("Enter your choice (1-4): "))

            if user_choice == 1:
                print("Current Balance: ₹", round(account_balance, 2))

            elif user_choice == 2:
                account_balance = deposit(account_balance)

            elif user_choice == 3:
                account_balance = withdraw(account_balance)

            elif user_choice == 4:
                print("Thank you for using ATM. Goodbye!")
                break

            else:
                print("Invalid choice. Please select between 1 and 4.")

        except ValueError:
            print("Invalid input! Please enter a number between 1 and 4.")


# Run the program
main()