print("--- Welcome to the Divider Program ---")
divisor = input("Enter a number to divide 100 by: ")

try:
    number = int(divisor)

    result = 100 / number
    print(f"The result is {result}")

except ValueError:
    print("Error: That is not a number! Please enter digits only.")

except ZeroDivisionError:
    print("Math error: You cannot divide by zero!")

except Exception as e:
    print(f"An unexpected error occurred: {e}")