# M10 Database

## The "Why?"

Variables and lists are great for temporary data, but they disappear the moment your program stops running. Files (like CSV or JSON) are good for simple storage, but they can become slow and difficult to manage as your data grows. **Databases** are designed for high-performance, permanent storage and complex queries. **SQLite** is a lightweight database that comes built-in with Python, requiring no complex setup. It is used in everything from mobile apps to web browsers to store information safely and efficiently.

## Goals

Understand how to create a database file, define tables to structure your data, insert new records, and retrieve information using basic **SQL** (Structured Query Language).

## Core Concepts

### SQLite
SQLite is a "serverless" database engine. The entire database is contained within a single file (usually ending in `.db`) on your computer, making it highly portable.

### SQL (Structured Query Language)
To talk to a database, we use SQL commands:
- `CREATE TABLE`: Defines the "blueprint" (columns and types) of your data.
- `INSERT INTO`: Adds a new row of data.
- `SELECT * FROM`: Retrieves data from the table.

### Connection and Cursor
- **Connection**: Represents the "bridge" between your Python script and the database file.
- **Cursor**: Acts like a "worker" that executes your SQL commands and fetches the results.

## Guided Practice

We will build a simple **Contact Book** system that saves names and phone numbers to a permanent database file.

*   **Step 1: Create `contact_manager_example.py`**
    ```python
    import sqlite3
    import os

    # Move to the current script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 1. Connect to the database file
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()

    # 2. Create a table (if it doesn't already exist)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT
        )
    ''')

    # 3. Insert a new record
    # We use '?' as placeholders to prevent security issues (SQL Injection)
    name_input = "Alice Smith"
    phone_input = "555-0199"

    # Check if the record already exists before adding
    cursor.execute("SELECT * FROM people WHERE name = ?", (name_input,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO people (name, phone) VALUES (?, ?)", (name_input, phone_input))
        # 4. Save (commit) the changes
        conn.commit()
        print(f"Success: Added {name_input} to the database.")
    else:
        print(f"Note: {name_input} already exists in the database.")

    # 5. Retrieve and display data
    cursor.execute("SELECT * FROM people")
    all_contacts = cursor.fetchall()

    print("\n--- Current Contact List ---")
    for contact in all_contacts:
        print(f"ID: {contact[0]} | Name: {contact[1]} | Phone: {contact[2]}")

    # 6. Always close the connection when finished
    conn.close()
    print("\nDatabase connection closed.")
    ```

## Checkpoints

* [ ] **Dynamic Inserter**:
    Modify the script to ask the user for a name and phone number via `input()`, then save that input directly into the database.
* [ ] **The Searcher**:
    Write a script that asks for a name, then uses the `SELECT` command with a `WHERE` clause to find and print only that specific person's phone number.
* [ ] **Cleanup Crew**:
    Research how to use the `DELETE FROM` SQL command. Write a script that asks the user for an ID number and removes that record from the `people` table.