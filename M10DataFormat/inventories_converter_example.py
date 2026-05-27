import csv
import json

inventories = []

try:
    with open('inventories.csv', mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            row['price'] = float(row['price'])
            row['quantity'] = int(row['quantity'])
            inventories.append(row)

    with open('inventories.json', mode='w', encoding='utf-8') as json_file:
        json.dump(inventories, json_file, indent=4)

    print("Successfully converted inventories.csv to inventories.json!")
    print(f"Total items processed: {len(inventories)}")

except FileNotFoundError:
    print("Error: 'inventories.csv' not found. Please create it first.")