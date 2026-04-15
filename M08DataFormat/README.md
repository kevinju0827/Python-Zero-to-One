# M08 Data Format

## The "Why?"

Programs rarely exist in a vacuum. To be useful, they need to save data (like a high score in a game), read configuration (like your username), or exchange information with other systems (like a weather API). The two most common ways to represent this data are **CSV** (Comma-Separated Values) and **JSON** (JavaScript Object Notation). Understanding these formats allows your Python scripts to communicate with spreadsheets, databases, and web services globally.

## Goals

Learn how to use Python's built-in `csv` and `json` modules to read and write structured data, converting between external files and Python objects like Lists and Dictionaries.

## Core Concepts

### CSV (Comma-Separated Values)
CSV is the "universal language" of spreadsheets. Each line in a file is a record, and each record is divided into fields by commas.
- `csv.DictReader`: Reads rows as Dictionaries, using the header row as keys.
- `csv.DictWriter`: Writes Dictionaries to a CSV file.

### JSON (JavaScript Object Notation)
JSON is the standard format for web APIs. It looks almost identical to a Python Dictionary, making it incredibly easy to work with in Python.
- `json.load()`: Reads JSON from a file into a Python object.
- `json.dump()`: Writes a Python object to a JSON file.
- `json.loads()` / `json.dumps()`: Works with JSON strings instead of files.

## Guided Practice

In this practice, we will act as a bridge between an old spreadsheet-based inventory system and a modern web application. We will read a CSV file of products and convert it into a JSON format.

*   **Step 1: Create the sample CSV**
    Create a file named `inventory.csv`:
    ```csv
    id,name,price,quantity
    1,Laptop,1200,5
    2,Mouse,25,50
    3,Keyboard,75,20
    ```

*   **Step 2: Write the conversion script**
    Create a file named `inventory_converter_example.py`:
    ```python
    import csv
    import json

    inventory = []

    # 1. Read from CSV
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
    ```

## Checkpoints

* [ ] **Quick Data Entry**:
    Write a script that asks the user for their name, age, and city, then appends this information as a new row to a file named `users.csv`.
* [ ] **Config Reader**:
    Create a file named `config.json` with some settings (e.g., `{"theme": "dark", "notifications": true}`). Write a Python script that reads this file and prints a message based on the settings.
* [ ] **Data Sanitizer**:
    Read a JSON file containing a list of users. Filter out any users who are under 18 years old and print the remaining names.