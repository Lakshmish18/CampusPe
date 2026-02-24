#Palindrome Checker
#The program checks whether the entered string is a palindrom or not 

text = input("Enter a string: ")

processed_text = text.replace(" ", "").lower()  #Removes spaces & ignore case

if processed_text == processed_text[::-1]:     #Compares with reversed string
    print("It is a Palindrome.")
else:
    print("It is NOT a Palindrome.")