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

We will build the data layer for a small **personal expense tracker**—the kind of tool a freelancer might use to record purchases, answer the accountant's questions, and fix typos a week after the fact. One script will walk through every CRUD operation in sequence so you see how the pieces connect.

**Scenario**: You just signed your first freelance contract and want to start tracking deductible business expenses. By the end of the script, you should be able to (1) create a table, (2) seed sample data on first run, (3) answer three real questions the accountant might ask, and (4) safely fix a row and delete an accidental duplicate.

**Step 1: Set up the connection and table.** Use `sqlite3.connect("expenses.db")` to open (or create) the database. Run `CREATE TABLE IF NOT EXISTS expenses (...)` with these columns: `id` (auto-incrementing primary key), `spent_on` (ISO date text), `category`, `description`, and `amount` (REAL, NOT NULL).

**Step 2: Seed the database only on the first run.** Check `SELECT COUNT(*) FROM expenses` first. If the table is empty, `executemany()` a list of five sample rows that span at least two months and three categories. Always use `?` placeholders—never f-string user data into SQL.

**Step 3: Answer three realistic questions with SQL.**
1. *"What software did I buy in March?"* — `WHERE category = ? AND spent_on LIKE ?` with `'2026-03-%'`.
2. *"What is my Q1 transport total?"* — use SQL's `SUM()` aggregate with `BETWEEN ? AND ?`.
3. *"What was my single biggest expense this year?"* — `ORDER BY amount DESC LIMIT 1`.

**Step 4: Fix a mistake, then remove a duplicate.** Insert two rows that simulate the problem, then run `UPDATE expenses SET category = ? WHERE id = ?` on the first, and `DELETE FROM expenses WHERE id = ?` on the second. Always `commit()` at the end—without it, none of your changes are saved.

The full implementation is in `expense_tracker_example.py`. Read it section by section and run it twice: the first run seeds data, the second confirms persistence.

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
