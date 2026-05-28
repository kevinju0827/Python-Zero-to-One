def calculate_parking_fee(hours, daily_max=30):
    if hours <= 2:
        total_fee = 5
    else:
        extra_hours = hours - 2
        total_fee = 5 + (extra_hours * 3)
    return min(total_fee, daily_max)


while True:
    user_input = input("\nEnter parking hours (or 'q' to quit): ")

    if user_input.lower() == "q":
        print("Goodbye!")
        break

    try:
        hours = float(user_input)
        fee   = calculate_parking_fee(hours)
        print(f"Hours parked: {hours:.1f}")
        print(f"Total fee:    ${fee:.2f}")
    except ValueError:
        print("Please enter a valid number.")
