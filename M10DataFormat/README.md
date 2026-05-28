# M10 Data Formats

![Module 10 of 16](https://img.shields.io/badge/Module-10_of_16-6366f1?style=flat-square)
![Beginner](https://img.shields.io/badge/Difficulty-Beginner-4ade80?style=flat-square)
![1.5 hours](https://img.shields.io/badge/Time-1.5_hours-60a5fa?style=flat-square)
![Prerequisites: M09 — file I/O & pip](https://img.shields.io/badge/Prerequisites-M09:_file_I%2FO_%26_pip-94a3b8?style=flat-square)

**Topics covered:** CSV format · `csv.reader` / `DictReader` / `writer` · JSON format · `json.load` / `dump` / `loads` / `dumps` · type conversion when reading structured files

## The Why?

Programs rarely run in isolation. They need to save state (a high score, a configuration, a report), share data with other tools (a spreadsheet, a web API, another program), and exchange information across machines.

Two formats handle the vast majority of structured data in the real world:

- **CSV** (Comma-Separated Values) —the universal language of spreadsheets and tabular data
- **JSON** (JavaScript Object Notation) —the universal language of web APIs and configuration files

Once you can read and write both, your Python scripts can communicate with Excel, Google Sheets, REST APIs, databases, and virtually any modern software system. This module builds directly on the file I/O from M09 and the dict structure from M04.

---

## Core Concepts

### CSV —Tabular Data as Plain Text

A CSV file is a spreadsheet stripped of all formatting. Each line is a row; commas separate columns.

**Spreadsheet view:**

| id | name | price | quantity |
|----|------|-------|----------|
| 1  | Laptop | 1200 | 5 |
| 2  | Mouse | 25 | 50 |

**CSV file:**
```csv
id,name,price,quantity
1,Laptop,1200,5
2,Mouse,25,50
```

Python's built-in `csv` module handles the complexity of quoted fields, special characters, and different line endings.

**Reading with `csv.reader` (rows as lists):**

```python
import csv

with open("products.csv", mode="r", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)   # Skip the header row
    for row in reader:
        # row is a list: ['1', 'Laptop', '1200', '5']
        print(f"Name: {row[1]}, Price: {float(row[2]):.2f}")
```

**Reading with `csv.DictReader` (rows as dicts —recommended):**

```python
import csv

with open("products.csv", mode="r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # row is a dict: {'id': '1', 'name': 'Laptop', 'price': '1200', 'quantity': '5'}
        print(f"Name: {row['name']}, Price: {float(row['price']):.2f}")
```

`DictReader` uses the first row as keys —you access columns by name, not by fragile index numbers.

**Writing with `csv.DictWriter`:**

```python
import csv

products = [
    {"id": 1, "name": "Keyboard", "price": 75, "quantity": 20},
    {"id": 2, "name": "Monitor",  "price": 350, "quantity": 8},
]

with open("output.csv", mode="w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "name", "price", "quantity"])
    writer.writeheader()    # Write the first row (column names)
    writer.writerows(products)
```

> **Important:** always include `newline=""` when opening CSV files to prevent blank lines between rows on Windows.

> **Crucial note:** everything read from a CSV is a **string**. `row['price']` is `"1200"`, not `1200`. Always convert to `int()` or `float()` before doing math.

---

### JSON —Structured Data as Text

JSON looks almost exactly like Python dicts and lists —because it was inspired by them.

**JSON file:**
```json
{
    "name": "Laptop",
    "price": 1200,
    "in_stock": true,
    "tags": ["electronics", "computers"]
}
```

Python's built-in `json` module converts between JSON text and Python objects:

| Function | Direction | Usage |
|----------|-----------|-------|
| `json.load(f)` | File —Python dict/list | Reading a `.json` file |
| `json.dump(data, f)` | Python —File | Writing a `.json` file |
| `json.loads(string)` | String —Python | Parsing JSON text in memory |
| `json.dumps(data)` | Python —String | Converting to JSON string |

```python
import json

# Reading from a file
with open("config.json", mode="r", encoding="utf-8") as f:
    config = json.load(f)
    print(config["name"])   # "Laptop"

# Writing to a file
data = {"version": 2, "users": ["Alice", "Bob"]}
with open("output.json", mode="w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
```

`indent=4` makes the output human-readable instead of one compressed line.
`ensure_ascii=False` preserves Chinese, Japanese, and other non-ASCII characters.

---

## Going Further

<details>
<summary>Handling Non-UTF-8 Files</summary>

Files produced by Windows Excel sometimes use `cp1252` or `gbk` encoding. If `utf-8` fails:

```python
# Try utf-8-sig to handle BOM (Byte Order Mark) from Excel
with open("excel_export.csv", mode="r", encoding="utf-8-sig") as f:
    ...
```

</details>

<details>
<summary>Nested and Complex JSON</summary>

Real API responses often contain nested objects. Access them by chaining keys:

```python
data = {
    "user": {
        "name": "Alice",
        "address": {"city": "Taipei", "zip": "100"}
    }
}
print(data["user"]["address"]["city"])   # Taipei
```

</details>

<details>
<summary>CSV Dialects —Semicolon Separators</summary>

Some European software uses `;` instead of `,`. Specify the delimiter:

```python
csv.reader(f, delimiter=";")
csv.DictWriter(f, fieldnames=fields, delimiter=";")
```

</details>

<details>
<summary>`json.dumps()` for API Responses</summary>

When building web APIs (M13), you will often convert Python data to a JSON string to send as an HTTP response:

```python
response_body = json.dumps({"status": "ok", "count": 42}, indent=2)
```

</details>

<details>
<summary>Asking AI About Data Formats</summary>

Useful prompts:
- *"I have a CSV with columns A, B, C. Write Python code to read it as a list of dicts, convert column B to float, and save it as JSON."*
- *"This JSON has nested arrays. Write code to flatten it into a list of dicts for a CSV."*

</details>

---

## Guided Practice

**Scenario:** The sales team maintains product inventory in a CSV file updated in Excel, but the front-end developer on your team only works with JSON. You need an automated bridge that converts the CSV to clean, type-correct JSON every time the file changes — no copy-pasting between formats. We will build an **inventory converter** that reads `inventories.csv`, fixes the types, and exports a clean `inventory.json`.

### Step 1 —Create the input CSV

Create `inventories.csv` with this content:

```csv
id,name,price,quantity
1,Laptop,1200.00,5
2,Mouse,25.00,50
3,Keyboard,75.00,20
4,Monitor,350.00,8
```

### Step 2 —Read the CSV and fix types

Create `inventories_converter_example.py`:

```python
import csv
import json

products = []

with open("inventories.csv", mode="r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        products.append({
            "id":       int(row["id"]),
            "name":     row["name"],
            "price":    float(row["price"]),
            "quantity": int(row["quantity"]),
        })

print(f"Read {len(products)} products from CSV.")
print("Sample:", products[0])
```

Run the script. Confirm the types are correct (`price` should be a float, not a string).

### Step 3 —Export to JSON

Append this code to write the clean data to a JSON file:

```python
with open("inventory.json", mode="w", encoding="utf-8") as f:
    json.dump(products, f, indent=4, ensure_ascii=False)

print("Exported to inventory.json")
```

Open `inventory.json` and verify the formatting.

### Step 4 —Read the JSON back

Add a verification step that reads the JSON and prints a summary:

```python
with open("inventory.json", mode="r", encoding="utf-8") as f:
    loaded = json.load(f)

total_value = sum(p["price"] * p["quantity"] for p in loaded)
print(f"\nInventory summary: {len(loaded)} products, total value: ${total_value:,.2f}")
```

---

## Checkpoints

* [ ] **Sales Revenue Calculator**
  Create a `daily_sales.csv` with columns: `date`, `product_name`, `quantity`, `unit_price`.
  Write a script that reads it, calculates `revenue = quantity * unit_price` for each row, and prints a grand total.
  *(Remember: CSV values are always strings —convert before multiplying.)*

* [ ] **Config File Manager**
  Create a `settings.json` with keys like `username`, `theme`, `language`, `notifications_enabled`.
  Write a script that:
  1. Loads the config on startup and prints the current settings.
  2. Asks the user if they want to change the `theme` (light/dark).
  3. Updates the value in the dict and saves it back to the file.
  Run the script twice to confirm the change persists between runs.

* [ ] **JSON —CSV Transformer**
  Given a JSON file containing a list of objects (you can generate it from an API response or write one manually), write a script that reads the JSON and writes it out as a clean CSV file with a proper header row.
  *(Hint: use `data[0].keys()` to get the column names from the first record.)*
