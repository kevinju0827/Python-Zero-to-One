total_cost = 500.00

while True:
    try:
        qty = int(input("Quantity received: "))
        if qty <= 0:
            raise ValueError("Quantity must be a positive number.")
        unit_price = total_cost / qty
        print(f"Unit price: ${unit_price:.2f}")
        break
    except ValueError as e:
        print(f"Invalid input: {e}. Please try again.")
    finally:
        print("--- Input attempt recorded ---")
