total_cost = 500.00
user_input = input("Enter the quantity of items received: ")

try:
    quantity = int(user_input)
    unit_price = total_cost / quantity
    print(f"The unit price is ${unit_price}")
except ValueError:
    print("System Error: Invalid quantity format. Please enter numerical digits only.")
except ZeroDivisionError:
    print("System Error: Quantity cannot be zero. Cannot calculate unit price for an empty shipment.")