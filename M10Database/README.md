# M10 Database

## The "Why?"

In M08, you learned how to save data into CSV and JSON files. That works perfectly when your dataset is small and you only need to read it from top to bottom. But the moment your data starts to grow—imagine an online store with 500,000 orders, or a contact app shared between three people on different computers—plain files start breaking down. Searching for "all orders placed by Alice in March" forces you to load the entire file into memory and loop through every single row. If two scripts try to update the file at the same time, your data can become silently corrupted.

A **database** is a piece of software specifically engineered to solve these problems. It can search through millions of rows in milliseconds, guarantees that updates either fully succeed or fully fail (never half-applied), and allows multiple programs to safely read and write at the same time. **SQLite**—Python's built-in database—is the most widely deployed database engine in the world. It quietly powers your web browser's history, your phone's text messages, the in-flight entertainment system on most airplanes, and countless desktop applications. Once you learn it, the same skills transfer almost identically to enterprise databases like PostgreSQL or MySQL.

## Goals

By the end of this module, you should be able to:

* Explain why a database is preferable to a flat file once data grows or needs to be shared.
* Describe what SQLite is and why it is suitable for local, single-file storage.
* Use Python's built-in `sqlite3` module to connect to a database and obtain a cursor.
* Write basic SQL statements to **C**reate, **R**ead, **U**pdate, and **D**elete records (the "CRUD" operations).
* Use parameterized queries (`?` placeholders) to safely insert user input into SQL statements.
* Understand the role of `commit()` and why changes are not saved until you call it.
* Use `WHERE`, `ORDER BY`, and `LIMIT` clauses to filter and shape results.

## Core Concepts

### What Makes a Database Different from a File?

A CSV file is just text. To find a row, your program has to read the whole file and check every line. A database, by contrast, stores data in structured **tables** and maintains internal indexes that act like the index at the back of a textbook—it can jump straight to the right rows without scanning everything.

Three other guarantees a database gives you that a file does not:

* **Schema enforcement**: When you define a column as `INTEGER NOT NULL`, the database will refuse to store text or empty values there. CSV files happily store anything you type.
* **Atomic transactions**: A group of related changes either all succeed or all fail. If your bank transfer script crashes after deducting money but before adding it to the other account, a database can roll back the change. A CSV file cannot.
* **Concurrent access**: Multiple programs can safely read and write at the same time without overwriting each other.

### SQLite: A Database in a Single File

Most databases run as a separate server program that you connect to over the network (PostgreSQL, MySQL, etc.). **SQLite** is different—it lives entirely inside a single `.db` file on your hard drive, and you talk to it directly from your Python script using the built-in `sqlite3` module. No installation, no server, no configuration.

This makes SQLite ideal for:

* Personal tools and desktop apps that don't need to be shared over a network.
* Prototyping ideas before scaling up to a "real" database.
* Storing application settings, caches, or logs.

### SQL: The Language of Databases

**SQL** (Structured Query Language) is the language you use to ask a database to do things. The four core operations are often called **CRUD**:

| Operation  | SQL Keyword | Real-World Analogy                     |
|------------|-------------|----------------------------------------|
| **C**reate | `INSERT`    | Adding a new row to a spreadsheet      |
| **R**ead   | `SELECT`    | Looking up rows that match a condition |
| **U**pdate | `UPDATE`    | Editing the value of an existing cell  |
| **D**elete | `DELETE`    | Removing a row from a spreadsheet      |

Before you can do any of these, the table must exist. You define it once using `CREATE TABLE`:

```sql
CREATE TABLE IF NOT EXISTS people (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL,
    phone   TEXT
)
```

Each column has a **type** (`INTEGER`, `TEXT`, `REAL`, etc.) and optional **constraints** (`NOT NULL` means the field is required; `PRIMARY KEY AUTOINCREMENT` means SQLite will assign a unique, ever-increasing ID for you).

---

### Connection and Cursor: How Python Talks to SQLite

Two objects do all the work:

* **Connection**: Represents the open "bridge" between your script and the `.db` file. You create it with `sqlite3.connect('your_file.db')`. If the file doesn't exist, SQLite creates it.
* **Cursor**: A worker you ask to actually run SQL commands. You get one by calling `conn.cursor()`. The cursor's `execute()` method runs a query; `fetchone()` returns a single row; `fetchall()` returns every row from the most recent `SELECT`.

```python
import sqlite3

conn = sqlite3.connect('example.db')   # Open the connection (creates file if missing)
cursor = conn.cursor()                  # Get a cursor to run commands
cursor.execute("SELECT * FROM people")  # Run a query
rows = cursor.fetchall()                # Collect the results
conn.close()                            # Always close when finished
```

---

### Parameterized Queries: The Most Important Habit You Will Form

Never build SQL queries by gluing strings together with user input. Doing so opens the door to **SQL injection**—an attacker can type carefully crafted text into your input field and trick your database into running commands you never intended (including dropping the whole table).

**Wrong** (vulnerable, never do this):

```python
name = input("Search for: ")
cursor.execute(f"SELECT * FROM people WHERE name = '{name}'")  # DANGEROUS
```

**Right** (use `?` placeholders):

```python
name = input("Search for: ")
cursor.execute("SELECT * FROM people WHERE name = ?", (name,))
```

The `sqlite3` module safely escapes the value for you. The tuple `(name,)`—note the comma—is required even when there is only one placeholder.

---

### `commit()`: Why Your Changes Disappear If You Forget

When you run `INSERT`, `UPDATE`, or `DELETE`, SQLite stages the change in a temporary **transaction** but does *not* permanently write it to the file until you call `conn.commit()`. If your script crashes (or you forget to commit), the change is silently discarded.

```python
cursor.execute("INSERT INTO people (name) VALUES (?)", ("Bob",))
conn.commit()   # Without this, Bob is NOT saved
```

This is a feature, not a bug: it lets you bundle multiple statements together as a single atomic unit. If anything in the bundle fails, you can call `conn.rollback()` to undo all of them.

---

### Filtering and Shaping Results

A bare `SELECT * FROM people` returns every row. In practice, you almost always want to narrow the result:

| Clause     | What It Does                          | Example                                |
|------------|---------------------------------------|----------------------------------------|
| `WHERE`    | Keep only rows matching a condition   | `WHERE age > 30`                       |
| `ORDER BY` | Sort the results                      | `ORDER BY name ASC` (or `DESC`)        |
| `LIMIT`    | Return at most N rows                 | `LIMIT 10`                             |

```python
cursor.execute(
    "SELECT name, phone FROM people WHERE name LIKE ? ORDER BY name ASC LIMIT 5",
    ('A%',)   # Names starting with 'A'
)
```

---

## Guided Practice

At the very top of your file, we need to import Python's built-in database module and ensure that our database file is always created in the exact same directory as our script.

```python
import os
import sqlite3

# Ensure expenses.db is kept next to this script regardless of where Python is launched from
os.chdir(os.path.dirname(os.path.abspath(__file__)))

```

## Step 1: Establish Connection and Create Table (Create)

We will now build a bridge to our database and define the layout of our spreadsheet-like table.
Append this code to your file:

```python
# 1. Connect to the database (creates the file if it's missing)
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()  # Get our database assistant

# 2. Define the database table layout
cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id           INTEGER PRIMARY KEY AUTOINCREMENT, -- A unique ID automatically handled by SQLite
        spent_on     TEXT NOT NULL,    -- Date format 'YYYY-MM-DD' so it sorts correctly
        category     TEXT NOT NULL,    -- Expense category (e.g., software, transport)
        description  TEXT,             -- Optional notes
        amount       REAL NOT NULL     -- Cost as a decimal/floating point number
    )
""")
print("Step 1 Complete: Database and table are ready!")

```

---

## Step 2: Safely Seed Initial Data (Insert)

Now that the table exists, let's populate it with some initial mock expenses for a freelancer.
```python
# Sample records spanning multiple dates and categories
sample_rows = [
    ("2026-01-12", "software",  "Adobe subscription",     19.99),
    ("2026-01-22", "transport", "Taxi to client meeting", 18.50),
    ("2026-02-05", "meal",      "Coffee with prospect",    7.20),
    ("2026-03-03", "software",  "JetBrains licence",      89.00),
    ("2026-03-18", "transport", "Train ticket — Tainan",  35.40),
]

# Check if data already exists so we don't duplicate rows every time we run the script
existing = cursor.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]

if existing == 0:
    # Use executemany to safely insert multiple rows via '?' placeholders
    cursor.executemany(
        "INSERT INTO expenses (spent_on, category, description, amount) VALUES (?, ?, ?, ?)",
        sample_rows,
    )
    conn.commit() # 🌟 CRITICAL: Save changes to the disk!
    print(f"Step 2 Complete: Seeded {len(sample_rows)} initial sample rows.\n")
else:
    print(f"Step 2 Notice: Database already contains {existing} rows — skipping seed.\n")

```

---

## Step 3: Extract Answers From Your Data (Select)

Let's act like an accountant and query our database to answer three realistic business questions.
```python
print("=== Step 3: Querying the Database ===")

# Question 1: What software did I buy in March?
print("--- 1. March 2026 Software Expenses ---")
for date, description, amount in cursor.execute(
        "SELECT spent_on, description, amount FROM expenses "
        "WHERE category = ? AND spent_on LIKE ? ORDER BY spent_on",
        ("software", "2026-03-%"), # Maps directly to the '?' marks
):
    print(f"   Date: {date} | Item: {description:<20} | Amount: ${amount:>7.2f}")


# Question 2: What is my Q1 transport total?
total = cursor.execute(
    "SELECT SUM(amount) FROM expenses WHERE category = ? AND spent_on BETWEEN ? AND ?",
    ("transport", "2026-01-01", "2026-03-31"),
).fetchone()[0] or 0.0 # fetchone()[0] gets the single aggregated number

print(f"\n--- 2. Q1 Transport Total ---")
print(f"   Total Spend: ${total:.2f}")


# Question 3: What was my single biggest expense this year?
# Sort by amount descending (highest to lowest) and restrict results to 1 row
biggest = cursor.execute(
    "SELECT spent_on, category, description, amount FROM expenses "
    "WHERE spent_on LIKE ? ORDER BY amount DESC LIMIT 1",
    ("2026-%",), # 🌟 Remember the trailing comma!
).fetchone()

print(f"\n--- 3. Biggest Expense of the Year ---")
if biggest:
    date, category, description, amount = biggest
    print(f"   Top Expense: {date} [{category}] {description} (${amount:.2f})\n")

```

---

## Step 4: Fix Mistakes and Clean Up (Update & Delete)

Typos happen. Suppose we accidentally logged a "ChatGPT Subscription" twice, and we accidentally assigned it to the `meal` category instead of `software`. Here is how we remedy both issues.

```python
print("=== Step 4: Fixing Mistakes and Duplicates ===")

# Let's intentionally insert a miscategorized item and a duplicate entry to demonstrate the fix
cursor.execute("INSERT INTO expenses (spent_on, category, description, amount) VALUES (?, ?, ?, ?)",
               ("2026-05-10", "meal", "ChatGPT Plus subscription", 20.00))
wrong_id = cursor.lastrowid # Grabs the unique ID assigned to this newly created row

cursor.execute("INSERT INTO expenses (spent_on, category, description, amount) VALUES (?, ?, ?, ?)",
               ("2026-05-10", "meal", "ChatGPT Plus subscription", 20.00))
duplicate_id = cursor.lastrowid

# Action A: Fix the wrong category on our first entry by targeted ID
print(f" Fixing row #{wrong_id} (Changing category from 'meal' to 'software')...")
cursor.execute("UPDATE expenses SET category = ? WHERE id = ?", ("software", wrong_id))

# Action B: Purge the duplicate row entirely
print(f" Removing duplicate entry row #{duplicate_id}...")
cursor.execute("DELETE FROM expenses WHERE id = ?", (duplicate_id,))

# Commit all changes made in Step 4 and cleanly close the communication bridge
conn.commit()
conn.close()

print("\n🎉 Mission Accomplished! Your database script is complete and safely disconnected.")

```

---

## How to Verify Your Script Works

1. **Run the script the 1st time**:
Your console will output: `Seeded 5 initial sample rows.`, display the answers to the 3 analytical questions, and confirm the modification/deletion cycle.
2. **Run the script a 2nd time**:
You will notice the output changes to: `Database already contains X rows — skipping seed.`. This is solid proof that SQLite successfully preserved your data inside the persistent `expenses.db` file on your drive.

---

## Checkpoints

* [ ] **Personal Reading Log**:
      You are starting a habit of tracking every book you finish reading. Build a script that manages a `books` table with these columns: `id`, `title`, `author`, `genre`, `finished_on` (date as text), and `rating` (1–5).
      Your script should:
      1. On first run, create the table if it does not exist and insert at least four sample books across at least two different genres.
      2. Ask the user (via `input()`) to enter a **new** book they just finished and insert it.
      3. After insertion, display **all books they have read this year**, sorted from highest-rated to lowest.
      4. Print a one-line summary: `"You have finished N books this year, with an average rating of X.X."`
      *(Hint: use the SQL functions `COUNT()` and `AVG()` to compute the summary in a single query instead of looping in Python.)*

* [ ] **Mini Inventory Management Tool**:
      A small bookstore owner asks you to help manage their stock. Build a script that maintains a `products` table (`id`, `name`, `price`, `stock_quantity`) and offers a simple text-based menu in the terminal:
      ```
      1) Add a new product
      2) Sell a product (decrease stock by 1)
      3) Show all products with stock <= 5 (low-stock report)
      4) Quit
      ```
      Use a `while True` loop that calls `input()` for the menu choice and dispatches to a corresponding function. Selling a product should both decrement `stock_quantity` and refuse to go below zero (print an "out of stock" warning instead).
      *(Hint: use a `try/except sqlite3.IntegrityError` block if you decide to add `UNIQUE` or `CHECK` constraints—this is the kind of defensive code real applications need.)*

* [ ] **Daily Habit Streak Tracker**:
      Combine M07 (`datetime`) with what you just learned. Build a `habits` tracker where each row records the **date** the user marked the habit as "done." The script should:
      1. Each time it runs, ask which habit the user completed today (e.g., `"exercise"`, `"read"`, `"meditate"`).
      2. Refuse to insert a duplicate row for the same habit on the same day (use a `SELECT` check or a `UNIQUE` constraint).
      3. After logging, compute and print the user's **current streak** for that habit—the number of consecutive days, ending today, where they recorded it.
      *(Hint: fetch the dates in descending order and walk backwards using Python's `datetime.timedelta(days=1)` until you hit a gap. This combines SQL filtering with Python date arithmetic—exactly the kind of hybrid problem-solving real applications require.)*
