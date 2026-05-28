# M12 Database

![Module 12 of 16](https://img.shields.io/badge/Module-12_of_16-6366f1?style=flat-square)
![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-facc15?style=flat-square)
![~2 hours](https://img.shields.io/badge/Time-~2_hours-60a5fa?style=flat-square)
![Prerequisites: M11 — HTTP requests](https://img.shields.io/badge/Prerequisites-M11:_HTTP_requests-94a3b8?style=flat-square)

**Topics covered:** why databases beat flat files · SQLite · `sqlite3` module · SQL CRUD · parameterized queries · `commit()` · `WHERE` / `ORDER BY` / `LIMIT` · aggregate functions

## The Why?

In M10, you learned to save data to CSV and JSON files.
That works well when your data is small and you only read it from top to bottom.
But the moment your data grows —an online store with 500,000 orders, a contact app shared between multiple users —plain files start breaking down:

- **Searching is slow:** finding "all orders by Alice in March" means loading the entire file into memory and scanning every row.
- **No type safety:** CSV files happily store `"abc"` in a column that should be a price.
- **Concurrency is dangerous:** if two processes write to the same file simultaneously, data corrupts silently.

A **database** solves all three problems. It searches millions of rows in milliseconds, enforces data types, and guarantees that updates either fully succeed or fully fail (never half-applied).

**SQLite** is the world's most widely deployed database engine. It lives in a single `.db` file on your hard drive and requires no server or configuration. It quietly powers your web browser's history, your phone's text messages, and countless desktop applications. The same SQL skills you learn here transfer directly to PostgreSQL, MySQL, and every other enterprise database.

---

## Core Concepts

### What Makes a Database Different from a File?

Three guarantees a database provides that a CSV file cannot:

| Guarantee | What it means | CSV equivalent |
|-----------|---------------|---------------|
| **Schema enforcement** | `INTEGER NOT NULL` rejects letters | Anything goes |
| **Atomic transactions** | Changes either fully apply or fully rollback | Partial writes possible |
| **Fast queries** | Index-based lookups skip irrelevant rows | Scan everything |

---

### SQL —The Language of Databases

SQL (Structured Query Language) is how you talk to a database.
The four core operations are called **CRUD**:

| Operation | SQL Keyword | What it does |
|-----------|-------------|-------------|
| **C**reate | `INSERT` | Add a new row |
| **R**ead | `SELECT` | Query rows that match conditions |
| **U**pdate | `UPDATE` | Modify existing rows |
| **D**elete | `DELETE` | Remove rows |

Before any CRUD, you define the table structure with `CREATE TABLE`:

```sql
CREATE TABLE IF NOT EXISTS contacts (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT    NOT NULL,
    phone   TEXT,
    group   TEXT    DEFAULT 'other'
)
```

Each column has a **type** (`INTEGER`, `TEXT`, `REAL`) and optional **constraints** (`NOT NULL`, `DEFAULT`).
`PRIMARY KEY AUTOINCREMENT` means SQLite assigns a unique, ever-increasing ID automatically.

---

### Connection and Cursor

Two objects do all the work in Python:

```python
import sqlite3

conn   = sqlite3.connect("mydata.db")   # Opens/creates the .db file
cursor = conn.cursor()                   # The worker that runs SQL

cursor.execute("SELECT * FROM contacts")
rows = cursor.fetchall()                 # All results as a list of tuples

conn.close()                             # Always close when done
```

---

### Parameterized Queries —Non-Negotiable Safety

**Never** build SQL by concatenating user input. This creates an **SQL injection** vulnerability —an attacker can type crafted text that deletes your entire database.

```python
# DANGEROUS —never do this:
cursor.execute(f"SELECT * FROM contacts WHERE name = '{name}'")

# SAFE —always use ? placeholders:
cursor.execute("SELECT * FROM contacts WHERE name = ?", (name,))
```

The trailing comma in `(name,)` is required —even for a single value, it must be a tuple.

---

### `commit()` —Saving Changes

`INSERT`, `UPDATE`, and `DELETE` are staged in memory until you call `conn.commit()`.
Without it, changes disappear when the script exits.

```python
cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", ("Alice", "0912-111-222"))
conn.commit()   # Without this, Alice is NOT saved
```

---

### Filtering and Shaping Results

```python
# WHERE —filter rows
cursor.execute("SELECT * FROM contacts WHERE group = ?", ("work",))

# ORDER BY —sort results
cursor.execute("SELECT * FROM contacts ORDER BY name ASC")

# LIMIT —return at most N rows
cursor.execute("SELECT * FROM contacts ORDER BY name ASC LIMIT 10")

# Aggregate functions
cursor.execute("SELECT COUNT(*), AVG(rating) FROM books WHERE genre = ?", ("fiction",))
```

---

## Going Further

<details>
<summary>`row_factory` —Dict-Like Rows</summary>

By default, `fetchall()` returns tuples. Set `row_factory` for dict-like access:

```python
conn.row_factory = sqlite3.Row
cursor.execute("SELECT * FROM expenses")
for row in cursor.fetchall():
    print(row["description"], row["amount"])   # Access by column name
```

</details>

<details>
<summary>Using Connection as a Context Manager</summary>

```python
with sqlite3.connect("mydata.db") as conn:
    conn.execute("INSERT INTO ...")
    # commit() is called automatically when the with block exits cleanly
    # rollback() is called automatically if an exception occurs
```

</details>

<details>
<summary>Indexes —Making Queries Fast</summary>

Without an index, every `WHERE` clause scans the entire table. Create one for frequently-queried columns:

```sql
CREATE INDEX IF NOT EXISTS idx_category ON expenses(category);
```

</details>

<details>
<summary>Multiple Tables and JOIN</summary>

Real databases split data across tables to avoid duplication. A `JOIN` brings them back together:

```sql
SELECT orders.id, customers.name, orders.amount
FROM orders
JOIN customers ON orders.customer_id = customers.id
WHERE orders.amount > 100
```

</details>

---

## Guided Practice

**Scenario:** You are a freelancer tracking business expenses for year-end tax filing. Your current CSV spreadsheet keeps getting corrupted and is impossible to query by category or date range. A local SQLite database gives you instant filtering, running totals, and reliable persistence — with zero setup cost. We will build an **expense tracker** that demonstrates all four CRUD operations.

### Step 1 —Setup and table creation

Create `expense_tracker_example.py`:

```python
import os
import sqlite3

os.chdir(os.path.dirname(os.path.abspath(__file__)))

conn   = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        spent_on    TEXT    NOT NULL,
        category    TEXT    NOT NULL,
        description TEXT,
        amount      REAL    NOT NULL
    )
""")
print("Database ready.")
```

### Step 2 —Seed initial data (INSERT)

```python
sample_rows = [
    ("2026-01-12", "software",  "Adobe subscription",      19.99),
    ("2026-01-22", "transport", "Taxi to client meeting",   18.50),
    ("2026-02-05", "meal",      "Coffee with prospect",      7.20),
    ("2026-03-03", "software",  "JetBrains licence",        89.00),
    ("2026-03-18", "transport", "Train ticket —Tainan",    35.40),
]

existing = cursor.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
if existing == 0:
    cursor.executemany(
        "INSERT INTO expenses (spent_on, category, description, amount) VALUES (?, ?, ?, ?)",
        sample_rows
    )
    conn.commit()
    print(f"Seeded {len(sample_rows)} rows.")
else:
    print(f"Database already has {existing} rows —skipping seed.")
```

### Step 3 —Query data (SELECT)

```python
print("\n--- Software expenses in March ---")
for row in cursor.execute(
    "SELECT spent_on, description, amount FROM expenses "
    "WHERE category = ? AND spent_on LIKE ? ORDER BY spent_on",
    ("software", "2026-03-%")
):
    print(f"  {row[0]} | {row[1]:<25} | ${row[2]:>7.2f}")

total = cursor.execute(
    "SELECT SUM(amount) FROM expenses WHERE category = ?", ("transport",)
).fetchone()[0] or 0.0
print(f"\n--- Total transport spend: ${total:.2f} ---")
```

### Step 4 —Fix a mistake (UPDATE and DELETE)

```python
# Insert a miscategorized row
cursor.execute(
    "INSERT INTO expenses (spent_on, category, description, amount) VALUES (?, ?, ?, ?)",
    ("2026-05-10", "meal", "ChatGPT Plus subscription", 20.00)
)
wrong_id = cursor.lastrowid

# Fix the category
cursor.execute("UPDATE expenses SET category = ? WHERE id = ?", ("software", wrong_id))
print(f"\nFixed category on row #{wrong_id}.")

# Insert a duplicate, then delete it
cursor.execute(
    "INSERT INTO expenses (spent_on, category, description, amount) VALUES (?, ?, ?, ?)",
    ("2026-05-10", "software", "ChatGPT Plus subscription", 20.00)
)
dup_id = cursor.lastrowid
cursor.execute("DELETE FROM expenses WHERE id = ?", (dup_id,))
print(f"Removed duplicate row #{dup_id}.")

conn.commit()
conn.close()
print("\nDone. Run the script again to confirm data persisted.")
```

---

## Checkpoints

* [ ] **Personal Reading Log**
  Create a `books` table: `id`, `title`, `author`, `genre`, `finished_on`, `rating` (1–5).
  On first run, create the table and insert at least four sample books.
  Then ask the user to enter a new book they just finished and insert it.
  Print all books read this year, sorted highest-rated first.
  Print: `"You've finished N books, average rating X.X."`
  *(Hint: use SQL `COUNT()` and `AVG()` to compute the summary in one query.)*

* [ ] **Mini Inventory Tool**
  A bookstore owner needs a stock manager. Build a terminal menu with options:
  1. Add a new product
  2. Sell a product (decrease stock by 1, refuse if already 0)
  3. Show low-stock report (stock ≤ 5)
  4. Quit
  Use a `while True` loop and wrap database operations in `try/except` for robustness.

* [ ] **Habit Streak Tracker**
  Combine `datetime` (M09) with SQLite. Each row records a date when the user marked a habit "done."
  On each run, ask which habit they completed today.
  Refuse to insert a duplicate for the same habit on the same day.
  Calculate and print the **current streak** —consecutive days ending today with that habit logged.
  *(Hint: fetch dates in descending order and walk backwards using `timedelta(days=1)` until a gap appears.)*
