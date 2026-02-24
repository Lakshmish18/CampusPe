# Temperature Converter Program
""" This program converts temperature between
 Celsius, Fahrenheit, and Kelvin."""


# Function to convert temperature
def convert_temperature(value, unit):
    
    if unit == "C":
        fahrenheit = (value * 9/5) + 32
        kelvin = value + 273.15
        print("Fahrenheit:", round(fahrenheit, 2))
        print("Kelvin:", round(kelvin, 2))
    
    elif unit == "F":
        celsius = (value - 32) * 5/9
        kelvin = celsius + 273.15
        print("Celsius:", round(celsius, 2))
        print("Kelvin:", round(kelvin, 2))
    
    elif unit == "K":
        celsius = value - 273.15
        fahrenheit = (celsius * 9/5) + 32
        print("Celsius:", round(celsius, 2))
        print("Fahrenheit:", round(fahrenheit, 2))
    
    else:
        print("Invalid unit! Please enter C, F, or K.")


# Main function
def main():
    temperature_value = float(input("Enter temperature value: "))
    temperature_unit = input("Enter unit (C/F/K): ").upper()
    
    convert_temperature(temperature_value, temperature_unit)


# Run program
main()