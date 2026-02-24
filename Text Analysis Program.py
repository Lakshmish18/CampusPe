# Text Analysis Program
"""This program analyzes the given text and shows:
1. Character count
2. Word count
3. Sentence count
4. Vowel count
5. Consonant count
6. Count of a specific character"""

# Function to count the characters
def count_characters(text):
    return len(text)


# Function to count words
def count_words(text):
    words = text.split()  # spliting text based on spaces
    return len(words)


# Function to count the sentences
def count_sentences(text):
    sentence_count = 0
    for char in text:
        if char == '.' or char == '!' or char == '?':
            sentence_count += 1
    return sentence_count


# Function to count the vowels
def count_vowels(text):
    vowels = "aeiouAEIOU"
    vowel_count = 0
    for char in text:
        if char in vowels:
            vowel_count += 1
    return vowel_count


# Function to count the consonants
def count_consonants(text):
    vowels = "aeiouAEIOU"
    consonant_count = 0
    for char in text:
        if char.isalpha() and char not in vowels:
            consonant_count += 1
    return consonant_count


# Function to count a specific character
def count_specific_character(text, target_character):
    character_count = 0
    for char in text:
        if char == target_character:
            character_count += 1
    return character_count


# Main program
print("------ Text Analysis Tool ------")
user_text = input("Enter your text: ")

if user_text.strip() == "":
    print("No text entered.")
else:
    print("\nCharacter Count:", count_characters(user_text))
    print("Word Count:", count_words(user_text))
    print("Sentence Count:", count_sentences(user_text))
    print("Vowel Count:", count_vowels(user_text))
    print("Consonant Count:", count_consonants(user_text))

    # Asking user which character to count
    target_character = input("Enter a character to count: ")
    
    if len(target_character) == 1:
        print("Count of", target_character, ":", 
              count_specific_character(user_text, target_character))
    else:
        print("Please enter only a single character.")