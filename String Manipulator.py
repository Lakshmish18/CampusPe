"""String Manipulator Program 
This program performs 5 basic operations on a string entered by the user.
The 5 options r Uppercase, Lowercase, Reversing, Count, Palindrome."""

def string_manipulator():
    
    # Taking input from the user
    text = input("Enter a string: ")
    
    # First,checking if string is empty or not 
    if text == "":
        print("You entered an empty string.")
        return
    
    # Displaying menu
    print("\nSelect an operation:")
    print("1.Convert to Uppercase")
    print("2.Convert to Lowercase")
    print("3.Reversing  the String")
    print("4.Count Characters")
    print("5.Check Palindrome")
    
    choice = input("Enter your choice (1-5): ")
    
    # choice 1: Convert to uppercase
    if choice == "1":
        print("Uppercase:", text.upper())
    
    # choice 2: Convert to lowercase
    elif choice == "2":
        print("Lowercase:", text.lower())
    
    # choice 3: Reversing the  string
    elif choice == "3":
        reversed_text = text[::-1]   #we r using slicing to reverse
        print("Reversed String:", reversed_text)
    
    # choice 4: Count total characters
    elif choice == "4":
        print("Total number of characters:", len(text))
    
    # choice 5: Check palindrome
    elif choice == "5":
        # first convert to lowercase and remove spaces
        cleaned_text = text.replace(" ", "").lower()
        
        if cleaned_text == cleaned_text[::-1]:
            print("The string is a Palindrome.")
        else:
            print("The string is NOT a Palindrome.")
    
    else:
        print("Invalid choice. Please select between 1 to 5.")


# Calling the function
string_manipulator()