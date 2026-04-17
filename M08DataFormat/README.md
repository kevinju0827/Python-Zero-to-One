# M08 Data Format

## The "Why?"

Programs rarely exist in a vacuum. To be useful, they need to save data (like a high score in a game), read configuration (like your username), or exchange information with other systems (like a weather API). The two most common ways to represent this data are **CSV** (Comma-Separated Values) and **JSON** (JavaScript Object Notation). Understanding these formats allows your Python scripts to communicate with spreadsheets, databases, and web services globally.

## Goals

Learn how to use Python's built-in `csv` and `json` modules to read and write structured data, converting between external files and Python objects like Lists and Dictionaries.

Here is the expanded and beginner-friendly version of the `Core Concepts` section translated into English. You can copy and paste this directly to replace the `## Core Concepts` section in your README.md:

## Core Concepts

Before we learn how to process files, we need to understand what data looks like inside Python and how it is structured within external files.

### Prerequisite: Python Dictionaries (`dict`)

Think of a real-world dictionary: you look up a "word" to find its "definition." In Python, a **Dictionary (or `dict` for short)** works exactly the same way. It is a container used to store data in **Key-Value pairs**.

* **Key**: Like the word in a dictionary, it acts as a label. Keys are usually text strings (e.g., "name", "price").
* **Value**: Like the definition of the word, this is the actual data you want to store. It can be a number, a text string, a boolean (True/False), or even another list or dictionary.

**Example:**
```python
# This is a Python dictionary containing product information
product = {
    "name": "Laptop",    # The Key is "name", the Value is the string "Laptop"
    "price": 1200,       # The Key is "price", the Value is the number 1200
    "in_stock": True     # The Key is "in_stock", the Value is the boolean True
}

# We can retrieve the Value by using its Key
print(product["name"])   # Output: Laptop
```
Understanding Python dictionaries is crucial because the CSV and JSON data we are about to introduce are typically converted into dictionaries once loaded into Python!

### CSV (Comma-Separated Values)
**What is it?**
Think of a CSV file as a "plain-text Excel spreadsheet." It is one of the oldest and most universal ways to store tabular data. If you strip away all the fancy borders and colors from a spreadsheet, leaving only the raw data, you get a CSV:
1.  **Newlines** represent a "Row" (a single record of data).
2.  **Commas** are used to separate the different "Columns" (the fields).

**Visual Comparison:**
If your spreadsheet looks like this:

| id | name | price |
|---|---|---|
| 1 | Laptop | 1200 |

Its plain-text appearance in a CSV file will look exactly like this:
```text
id,name,price
1,Laptop,1200
```

**How does Python handle it?**
Python comes with a built-in `csv` module to help us read and write these files easily.
* `csv.DictReader`: Reads a CSV file. It is smart enough to use the first row (the headers) as Dictionary Keys, turning every subsequent row into a neat Python dictionary.
* `csv.DictWriter`: Takes your Python dictionaries and writes them back into the proper CSV file format.

### JSON (JavaScript Object Notation)

**What is it?**
Even though it has "JavaScript" in its name, JSON is now the "universal language" of the internet. When you scroll through social media or check a weather app, the data sent from the servers is almost always in JSON format.

JSON was designed to be easily parsed by machines, while still being easily readable by humans. **The best part for Python beginners is that JSON looks almost exactly like a Python Dictionary!**

**Visual Comparison:**
A piece of JSON data inside a file looks like this (wrapped in curly braces):
```json
{
    "id": 1,
    "name": "Laptop",
    "price": 1200
}
```

**How does Python handle it?**
Python has a built-in `json` module that allows you to seamlessly transition between "Python Dictionaries" and "JSON files."
* `json.load()`: Reads data from a JSON **file** and automatically converts it into a Python dictionary.
* `json.dump()`: Takes your Python dictionary and exports it, saving it as a standard JSON **file**.
* `json.loads()` / `json.dumps()`: The extra `s` stands for "string." You use these two tools when you want to convert between a Python dictionary and raw JSON text directly in your code, rather than interacting with a file.

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

*   **Step 2: Create `inventory_converter.py`**
    ```python
    import csv
    import json
    import os

    # 1. Ensure we are in the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    inventory = []

    # 2. Read from CSV
    try:
        with open('inventory.csv', mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                # Convert numeric strings to actual numbers
                row['price'] = float(row['price'])
                row['quantity'] = int(row['quantity'])
                inventory.append(row)

        # 3. Write to JSON
        with open('inventory.json', mode='w', encoding='utf-8') as json_file:
            json.dump(inventory, json_file, indent=4)

        print("Successfully converted inventory.csv to inventory.json!")
        print(f"Total items processed: {len(inventory)}")

    except FileNotFoundError:
        print("Error: 'inventory.csv' not found. Please create it first.")
    ```

## Checkpoints

* [ ] **Quick Data Entry**:
    Write a script that asks the user for their name, age, and city, then appends this information as a new row to a file named `users.csv`.
* [ ] **Config Reader**:
    Create a file named `config.json` with some settings (e.g., `{"theme": "dark", "notifications": true}`). Write a Python script that reads this file and prints a message based on the settings.
* [ ] **Data Sanitizer**:
    Read a JSON file containing a list of users. Filter out any users who are under 18 years old and print the remaining names.