# Grade Calculator Program
# Function to calculate total and average
def calculate_average(marks_list):
    total_marks = sum(marks_list)
    average_marks = total_marks / len(marks_list)
    return total_marks, average_marks


# Function to determine grade
def determine_grade(average_marks):
    if average_marks >= 90:
        return "A"
    elif average_marks >= 75:
        return "B"
    elif average_marks >= 60:
        return "C"
    elif average_marks >= 36:
        return "D"
    else:
        return "F"


# Main function
def main():
    number_of_subjects = int(input("Enter number of subjects: "))
    
    marks_list = []
    for i in range(number_of_subjects):
        mark = float(input(f"Enter marks for Subject {i+1}: "))
        marks_list.append(mark)
    
    # Calculating total and average
    total_marks, average_marks = calculate_average(marks_list)
    
    # Getting grade
    grade = determine_grade(average_marks)
    
    # Displaying results
    print("\nTotal Marks:", total_marks)
    print("Average Marks:", round(average_marks, 2))
    print("Grade:", grade)


# Run program
main()