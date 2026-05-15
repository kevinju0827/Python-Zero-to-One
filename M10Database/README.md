# M10 Database

## The "Why?"

In M08, you learned to save data in CSV and JSON files. Those formats work well for simple, one-time tasks—but they have a fundamental weakness: every time you want to find, update, or delete a specific record, your script must read the **entire file** into memory, scan through it line by line, make the change, and then rewrite the whole file back to disk. For a file with 100 rows, this is fine. For a file with 10 million rows, this is catastrophic.

This is the problem that **databases** were invented to solve. A database is a system designed from the ground up for one purpose: storing large amounts of structured data and retrieving exactly the piece you need, instantly, without ever loading everything else.

Beyond performance, databases also solve problems you might not have thought about yet:

* **Concurrent access**: What happens if two users try to update the same record at the same moment? A database handles this safely; a shared CSV file would be corrupted.
* **Data integrity**: How do you ensure a "price" column never accidentally contains the text "hello"? A database enforces rules; a file cannot.
* **Relationships**: How do you efficiently link a list of orders to the customers who placed them? Databases are built for exactly this.

In this module, we will use **SQLite**—a database that lives entirely inside a single file on your computer—to learn these concepts in a simple, zero-configuration environment. The skills you build here transfer directly to professional databases like PostgreSQL and MySQL.

## Goals

By the end of this module, you should be able to:

* Explain what a relational database is and describe the role of tables, rows, columns, and primary keys.
* Describe what SQLite is and why it is useful for learning and for small-scale applications.
* Use Python's built-in `sqlite3` module to create a database, define a table, and perform all four CRUD operations (Create, Read, Update, Delete).
* Use parameterized queries to safely insert user-supplied data into a database.
* Explain what SQL injection is and why parameterized queries prevent it.
* Configure a connection to return query results as dictionary-like objects instead of plain tuples.

## Core Concepts

### What is a Relational Database?

A **relational database** organizes data into one or more **tables**. If you understand spreadsheets, you are already halfway there—but the mental model breaks down in important ways, so let's be precise.

#### Table, Row, and Column

Imagine a physical filing cabinet. Each **table** is one drawer in the cabinet, dedicated to one category of information (e.g., "Products", "Customers", "Orders").

Inside that drawer, every **row** (also called a *record*) is one individual entry—one product, one customer, one order.

Every row is divided into **columns** (also called *fields*), which are the fixed categories of information each record must provide—like "name", "price", and "quantity".

The crucial rule is: **every row in the same table must have exactly the same columns.** You cannot add an extra "discount" field to just one product; you would have to add that column to the entire table.

**Visual Example:**

A `products` table might look like this:

| id | name     | price | quantity |
|----|----------|-------|----------|
| 1  | Laptop   | 1200  | 15       |
| 2  | Mouse    | 25    | 200      |
| 3  | Keyboard | 75    | 80       |

Each horizontal line is a **row**. Each vertical column (id, name, price, quantity) is a **column**. The entire grid is a **table**.

#### Primary Key

Notice the `id` column above. Every table needs a way to uniquely identify each row, because data like names and prices can repeat. The **primary key** is the column (or combination of columns) that guarantees uniqueness across all rows in the table.

Think of it like a national ID number: two people can share the same name, but no two people share the same ID number. The `id` column is almost always the primary key, and databases can be configured to assign a unique, incrementing number automatically so you never have to manage it yourself.

#### Data Types

Unlike a CSV file—where every single value is just text—a database column has a **data type** that it enforces. The most common types in SQLite are:

| SQLite Type | Stores                                    | Python Equivalent |
|-------------|-------------------------------------------|-------------------|
| `INTEGER`   | Whole numbers                             | `int`             |
| `REAL`      | Floating-point numbers                    | `float`           |
| `TEXT`      | Strings of any length                     | `str`             |
| `BLOB`      | Raw binary data (images, files, etc.)     | `bytes`           |
| `NULL`      | A missing or unknown value                | `None`            |

This is why, in M08, we had to manually convert CSV values with `int()` and `float()` after reading them. A database eliminates that problem entirely by storing and returning data already in the correct type.

#### Relationships Between Tables

The word "relational" in "relational database" refers to the ability to link tables together. For example, instead of duplicating customer information in every order row, you store customers in a `customers` table and orders in an `orders` table, and connect them with the customer's `id`.

This module focuses on a single table to keep things manageable. Relationships between multiple tables (called *joins*) are an important next step, but they build naturally on top of what you will learn here.

---

### What is SQLite?

Most databases run as a separate server process that your code connects to over a network—you need to install and configure the server, manage user accounts, and keep it running in the background. For learning, this is unnecessary complexity.

**SQLite** takes a completely different approach: the entire database—every table, every row, every index—is stored in a **single ordinary file** on your computer (e.g., `shop.db`). There is no server. There is no configuration. You simply open the file and start working.

This makes SQLite perfect for:
* **Learning**: Zero setup, immediate feedback.
* **Small applications**: Desktop apps, scripts, local tools.
* **Prototyping**: Build and test your data model before migrating to a larger database.

The tradeoff is that SQLite is not designed for high-traffic, multi-user scenarios. When you outgrow it, the concepts you have learned transfer directly to PostgreSQL or MySQL—the same logic, mostly the same syntax.

Python ships with SQLite support built in. You do not need to install anything.

```python
import sqlite3  # Part of the Python standard library — no pip install needed
```

---

### Connecting to a Database

Working with SQLite in Python involves two objects that you will use constantly:

* **Connection** (`sqlite3.connect()`): Opens (or creates) the database file. Think of this as opening the filing cabinet.
* **Cursor** (`connection.cursor()`): The tool you use to actually send instructions to the database and retrieve results. Think of this as your hand that reaches into the cabinet.

```python
import sqlite3

# This opens the file 'shop.db'. If it does not exist, SQLite creates it.
connection = sqlite3.connect('shop.db')

# Create a cursor — our interface for sending instructions
cursor = connection.cursor()

# ... do work here ...

# Always close the connection when you are done to free resources
connection.close()
```

Just like file handling in M08, it is best practice to use the `with` statement as a context manager. For SQLite, the `with` block handles an important additional responsibility: **committing or rolling back transactions** automatically.

```python
import sqlite3

# Using 'with' as a context manager:
# - If no exception occurs: automatically commits the transaction (saves changes)
# - If an exception occurs: automatically rolls back (undoes unsaved changes)
with sqlite3.connect('shop.db') as connection:
    cursor = connection.cursor()
    # ... do work here ...

# The connection is committed and closed automatically
```

> **What is a transaction?** A transaction is a group of database operations that are treated as a single, all-or-nothing unit. If you are deducting money from one account and adding it to another, both operations must succeed together—or neither should happen. SQLite wraps your operations in transactions automatically. `commit()` makes the changes permanent; `rollback()` undoes them.

---

### A Brief Word on SQL

To communicate with a database, you use a language called **SQL** (Structured Query Language). SQL is not a general-purpose programming language like Python—it is a specialized language for describing *what data you want*, not *how to get it*.

You do not need to master SQL to be productive. In Python, you write your SQL instructions as plain strings and pass them to the cursor. The four fundamental SQL operations map directly to CRUD:

| CRUD Operation | SQL Keyword | What It Does                         |
|----------------|-------------|--------------------------------------|
| **C**reate     | `INSERT`    | Add a new row to a table             |
| **R**ead       | `SELECT`    | Retrieve rows from a table           |
| **U**pdate     | `UPDATE`    | Modify existing rows                 |
| **D**elete     | `DELETE`    | Remove rows from a table             |

There is one additional keyword you need before you can do any of the above: `CREATE TABLE`, which defines the structure of a new table. Think of it as drawing the column headers on a blank spreadsheet before you start filling it in.

You will encounter these five keywords throughout this module. Everything else in SQL is built on top of them.

---

### Creating a Table

Before storing any data, you must define the table's structure: its name, its columns, and the data type of each column.

```python
import sqlite3

with sqlite3.connect('shop.db') as connection:
    cursor = connection.cursor()

    # cursor.execute() sends a single SQL instruction to the database.
    # We use triple quotes so the SQL string can span multiple lines cleanly.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT    NOT NULL,
            price     REAL    NOT NULL,
            quantity  INTEGER NOT NULL DEFAULT 0
        )
    ''')
```

Let's break down what each part means:

* `CREATE TABLE IF NOT EXISTS products`: Create a table named `products`, but only if it does not already exist. Without `IF NOT EXISTS`, running this script a second time would raise an error.
* `id INTEGER PRIMARY KEY AUTOINCREMENT`: The `id` column stores whole numbers, is the primary key (must be unique), and the database automatically assigns the next available number whenever a new row is inserted. You never have to set `id` yourself.
* `NOT NULL`: This column must always have a value. The database will reject any attempt to insert a row without a name or price.
* `DEFAULT 0`: If `quantity` is not provided when inserting, the database will automatically use `0` as the value.

---

### Inserting Data (Create)

To add a new row, you use `INSERT`. The most important thing to understand here is **parameterized queries**.

**The wrong way (never do this):**

```python
# ⚠️ DANGEROUS — Do not do this with user-supplied data
name = input('Product name: ')
cursor.execute(f"INSERT INTO products (name, price) VALUES ('{name}', 999)")
```

If a user types `'; DROP TABLE products; --` as their product name, this string gets injected directly into your SQL instruction and could destroy your entire database. This is called an **SQL injection attack**, and it is one of the most common security vulnerabilities in the world.

**The correct way — parameterized queries:**

```python
import sqlite3

with sqlite3.connect('shop.db') as connection:
    cursor = connection.cursor()

    # Use '?' as a placeholder. The actual values are passed separately as a tuple.
    # The database library handles the escaping — injection is impossible.
    cursor.execute(
        'INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)',
        ('Laptop', 1200.00, 15)
    )

    # To insert multiple rows at once, use executemany() with a list of tuples.
    more_products = [
        ('Mouse', 25.00, 200),
        ('Keyboard', 75.00, 80),
        ('Monitor', 399.00, 30),
    ]
    cursor.executemany(
        'INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)',
        more_products
    )

    print('Products inserted successfully.')
```

> **Rule**: Always use `?` placeholders. Never build SQL strings with f-strings or string concatenation when real data is involved.

---

### Querying Data (Read)

To retrieve rows, you use `SELECT`. After executing a `SELECT`, you retrieve the results through the cursor using one of three methods:

* `cursor.fetchone()`: Returns the next single row, or `None` if there are no more.
* `cursor.fetchall()`: Returns all remaining rows as a list.
* Iterating directly over the cursor: Memory-efficient for large result sets.

```python
import sqlite3

with sqlite3.connect('shop.db') as connection:
    cursor = connection.cursor()

    # Fetch all products
    cursor.execute('SELECT * FROM products')
    all_products = cursor.fetchall()

    for row in all_products:
        # By default, each row is a plain tuple: (1, 'Laptop', 1200.0, 15)
        print(row)

    # Fetch only one specific product using a WHERE clause
    cursor.execute('SELECT * FROM products WHERE id = ?', (1,))
    product = cursor.fetchone()
    print(f'Found: {product}')
```

Notice that `WHERE id = ?` uses the same `?` placeholder pattern. Any time you are filtering based on a value—especially one that came from outside your script—use a placeholder.

#### Getting Results as Dictionaries (Row Factory)

The default tuple format is inconvenient: you have to remember that index `[0]` is `id`, `[1]` is `name`, and so on. A much better approach is to configure the connection to return rows as dictionary-like objects, where you can access values by column name.

```python
import sqlite3

with sqlite3.connect('shop.db') as connection:

    # This one line changes everything: rows now behave like dictionaries
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM products')

    for row in cursor.fetchall():
        # Now we access values by column name, not index
        print(f'ID: {row["id"]} | {row["name"]} | ${row["price"]:.2f} | Qty: {row["quantity"]}')
```

Setting `connection.row_factory = sqlite3.Row` is considered best practice. Always set it immediately after opening the connection.

---

### Updating Data (Update)

To modify existing rows, you use `UPDATE` combined with `WHERE` to target only the specific rows you want to change. **Always include a `WHERE` clause**—omitting it would update every single row in the table.

```python
import sqlite3

with sqlite3.connect('shop.db') as connection:
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Update the price of the product with id = 1
    cursor.execute(
        'UPDATE products SET price = ? WHERE id = ?',
        (1099.00, 1)
    )

    # cursor.rowcount tells you how many rows were actually affected
    print(f'Rows updated: {cursor.rowcount}')

    # Verify the change
    cursor.execute('SELECT * FROM products WHERE id = ?', (1,))
    updated = cursor.fetchone()
    print(f'New price for {updated["name"]}: ${updated["price"]:.2f}')
```

---

### Deleting Data (Delete)

To remove rows, you use `DELETE` with a `WHERE` clause to identify which rows to remove. Again, **omitting `WHERE` would delete every row in the table**.

```python
import sqlite3

with sqlite3.connect('shop.db') as connection:
    cursor = connection.cursor()

    # Delete the product with id = 4
    cursor.execute('DELETE FROM products WHERE id = ?', (4,))

    print(f'Rows deleted: {cursor.rowcount}')
```

---

### Error Handling

Database operations can fail for many reasons: the file is locked by another process, a `NOT NULL` constraint is violated, a duplicate primary key is inserted, and so on. Wrap your database code in `try/except` blocks using the exception types from the `sqlite3` module.

```python
import sqlite3

try:
    with sqlite3.connect('shop.db') as connection:
        cursor = connection.cursor()

        # This will fail if a product with id=1 already exists
        cursor.execute(
            'INSERT INTO products (id, name, price, quantity) VALUES (?, ?, ?, ?)',
            (1, 'Duplicate Laptop', 999.00, 5)
        )

except sqlite3.IntegrityError as err:
    # Raised when a constraint is violated (e.g., duplicate primary key, NOT NULL)
    print(f'Data integrity error: {err}')

except sqlite3.OperationalError as err:
    # Raised for operational issues (e.g., table does not exist, database is locked)
    print(f'Operational error: {err}')

except sqlite3.Error as err:
    # The base class for all sqlite3 exceptions — catches anything we missed
    print(f'An unexpected database error occurred: {err}')
```

---

## Guided Practice

In this practice, we will build a **persistent contact book**—a script that stores contacts in a SQLite database and survives between runs. Unlike the in-memory Python lists you have used before, the data will still be there the next time you run the script.

### Step 1: Set Up the Database

Create a file called `contacts_db.py`. Begin by writing a setup function that opens (or creates) `contacts.db` and creates the `contacts` table if it does not already exist. The table should have five columns: `id`, `name`, `phone`, `email`, and `note`.

Call this function at the top of your script before doing anything else. This ensures the table always exists before we try to query it.

### Step 2: Add the "Add Contact" Feature

Write a function called `add_contact(name, phone, email, note)` that accepts the contact's details and inserts them as a new row using `executemany()` or `execute()` with `?` placeholders.

Test it by calling the function a few times with different contacts when your script first runs. Check that running the script a second time does not crash (because of `IF NOT EXISTS`) and does not add duplicate entries.

### Step 3: Add the "List All Contacts" Feature

Write a function called `list_contacts()` that queries all rows from the `contacts` table and prints each one in a clean, formatted layout. Remember to set `row_factory = sqlite3.Row` so you can access columns by name.

### Step 4: Add the "Search" Feature

Write a function called `search_contact(keyword)` that searches for contacts whose `name` contains the keyword. This introduces a new SQL pattern: the `LIKE` operator combined with `%` wildcard characters.

```python
# The % is a wildcard: it matches any sequence of characters.
# '%keyword%' means "contains 'keyword' anywhere in the value"
cursor.execute(
    "SELECT * FROM contacts WHERE name LIKE ?",
    (f'%{keyword}%',)
)
```

### Step 5: Add the "Delete Contact" Feature

Write a function called `delete_contact(contact_id)` that removes the row with the given `id`. After deleting, check `cursor.rowcount` and print either a success message or `"No contact found with that ID."` depending on the result.

### Step 6: Build a Simple Menu

Tie all the functions together with a `while True` loop that prints a menu, reads the user's choice with `input()`, and calls the appropriate function. The loop should only break when the user selects "Quit".

```
=== Contact Book ===
1. List all contacts
2. Add a contact
3. Search by name
4. Delete a contact
5. Quit
```

---

## Checkpoints

* [ ] **Personal Expense Tracker**:
      Build a command-line expense tracking tool backed by a SQLite database.
      Your database should have a single table called `expenses` with at least the following columns: `id`, `date`, `category`, `description`, and `amount`.
      Your script should support a menu-driven interface with these features:
      1. **Add an expense**: Prompt the user for the date, category (e.g., Food, Transport, Entertainment), description, and amount. Insert it into the database.
      2. **View all expenses**: Display every recorded expense in a clean, formatted table, sorted by date.
      3. **View expenses by category**: Ask the user to enter a category name and display only the matching expenses.
      4. **Show a summary**: Query and display the **total amount spent per category**, sorted from highest to lowest. This introduces `GROUP BY` — a SQL feature that groups rows sharing a common value before applying a calculation.
         > **Hint for the summary feature**: The SQL pattern looks like this:
         > ```sql
         > SELECT category, SUM(amount) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC
         > ```
         > You do not need to understand every word — focus on what the result looks like and how to display it in Python.
      5. **Delete an expense**: Ask the user for an expense `id` and remove it from the database.
      *(Additional challenge: After displaying "View all expenses", also print the grand total of all amounts at the bottom using Python's `sum()` on the fetched results — without making a second database query.)*