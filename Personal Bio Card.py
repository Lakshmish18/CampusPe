#Question-1: Personal Bio Card

while True:

    try:
        #in the try section we will take the inputs from the user 
        name = input("Enter your name: ")
        if name == "":
            print("Name shouldnt be  empty")
            continue

        age = int(input("Enter your age: "))
        if age <= 0:
            print("Age should be > 0")
            continue

        city = input("Enter your city: ")
        if city == "":
            print("plz enter the city name !")
            continue

        hobby = input("Enter your hobby: ")
        if hobby == "":
            print("--")
            continue

        # Printing the bio card
        print("\n------------------------------\n")
        print("        Personal Bio Card")
        print("------------------------------")
        print("Name  :", name)
        print("Age   :", age)
        print("City  :", city)
        print("Hobby :", hobby)
        print("------------------------------\n")

    except ValueError:
        # This error will occur when age is not a no. 
        print("Invalid input! Please enter numbers for age only.\n")

    # Asking user if  want to continue or not 
    choice = input("Do you want to enter another bio? (y/n): ")

    if choice.lower() != "y":
        print("Program ended.")
        break
