import sqlite3
import os

# Move to the current script directory to ensure the DB is created in this folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 1. Connect to the database file (created if it doesn't exist)
conn = sqlite3.connect('contacts.db')
cursor = conn.cursor()

# 2. Create a table using SQL (if it doesn't already exist)
# Tables structure the data into rows and columns
cursor.execute('''
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT
    )
''')

# 3. Add a new contact
# We use '?' placeholders to securely insert variables
name_input = "Alice Smith"
phone_input = "555-0199"

# Check if Alice is already in the database
cursor.execute("SELECT * FROM people WHERE name = ?", (name_input,))
if not cursor.fetchone():
    cursor.execute("INSERT INTO people (name, phone) VALUES (?, ?)", (name_input, phone_input))
    conn.commit()
    print(f"Success: Added {name_input} to the database.")
else:
    print(f"Note: {name_input} already exists in the database.")

# 4. Read all records back from the database
cursor.execute("SELECT * FROM people")
all_contacts = cursor.fetchall()

print("\n--- Current Contact List ---")
for contact in all_contacts:
    print(f"ID: {contact[0]} | Name: {contact[1]} | Phone: {contact[2]}")

# 5. Close the connection when done
conn.close()
print("\nDatabase connection closed.")
