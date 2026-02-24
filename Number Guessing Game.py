# Number Guessing Game
# The game generates a random number between 1 and 100.
# The user keeps guessing until the correct number is found.

import random
# here the random helps to generate a random number between the given range
def play_game():
    guessing_number = random.randint(1, 100)  # Random number between 1–100
    attempt_count = 0

    print("Guess the number between 1 and 100!")

    while True:
        try:
            user_guess = int(input("Enter your guess: "))
            attempt_count += 1

            if user_guess < 1 or user_guess > 100:
                print("Please guess within the range 1–100.")
            elif user_guess < guessing_number:
                print("Too low! Try again.")
            elif user_guess > guessing_number:
                print("Too high! Try again.")
            else:
                print(f"Correct! You guessed it in {attempt_count} attempts.")
                break

        except ValueError: # the imnput cant be like abc , @ , 5.6
            print("Invalid input! Please enter a valid integer.")

play_game()