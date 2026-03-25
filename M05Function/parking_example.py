def calculate_parking_fee(hours):
    if hours <= 2:
        total_fee = 5
    else:
        extra_hours = hours - 2
        total_fee = 5 + (extra_hours * 3)

    return total_fee


customer_fee = calculate_parking_fee(4)

print(f"You parked for 4 hours.")
print(f"Your total parking fee is: ${customer_fee}")