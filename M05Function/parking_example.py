def calculate_parking_fee(hours):
    if hours <= 2:
        total_fee = 5
    else:
        extra_hours = hours - 2
        total_fee = 5 + (extra_hours * 3)

    return total_fee

while True:
  user_input = input("Enter parking hours (or type 'q' to quit): ")

  if user_input.lower() == 'q':
      break

  input_hours = int(user_input)
  customer_fee = calculate_parking_fee(input_hours)

  print(f"You parked for {input_hours} hours.")
  print(f"Your total parking fee is: ${customer_fee}")
  print()