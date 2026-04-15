import csv
import json
import os

# Ensure we are in the correct directory relative to the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

inventory = []

# 1. Read from CSV
try:
    with open('inventory.csv', mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # Convert numeric strings to actual numbers
            row['price'] = float(row['price'])
            row['quantity'] = int(row['quantity'])
            inventory.append(row)

    # 2. Write to JSON
    with open('inventory.json', mode='w', encoding='utf-8') as json_file:
        json.dump(inventory, json_file, indent=4)

    print("Successfully converted inventory.csv to inventory.json!")
    print(f"Total items processed: {len(inventory)}")

except FileNotFoundError:
    print("Error: 'inventory.csv' not found. Please create it first.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
