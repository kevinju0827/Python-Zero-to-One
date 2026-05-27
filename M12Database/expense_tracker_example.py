"""M10 Guided Practice — A freelancer's expense tracker.

This one script walks through every CRUD operation against a real
SQLite database: it creates the table, seeds sample data, runs
representative queries (filter, sum, max), and demonstrates a safe
update + delete cycle.

Run it once to seed the database. Run it again to see that the seed
step is skipped and the queries still work against persistent data.
"""

import os
import sqlite3

# Keep expenses.db next to this script no matter where Python is launched from.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# -------------------------------------------------------------------------
# 1. CREATE — define the table once. IF NOT EXISTS makes this safe to re-run.
# -------------------------------------------------------------------------
cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        spent_on     TEXT NOT NULL,    -- ISO date 'YYYY-MM-DD' so string sort = date sort
        category     TEXT NOT NULL,
        description  TEXT,
        amount       REAL NOT NULL
    )
""")

# -------------------------------------------------------------------------
# 2. INSERT — seed sample rows only on the first run.
#    Parameterised '?' placeholders are how you safely combine SQL with data.
# -------------------------------------------------------------------------
sample_rows = [
    ("2026-01-12", "software",  "Adobe subscription",     19.99),
    ("2026-01-22", "transport", "Taxi to client meeting", 18.50),
    ("2026-02-05", "meal",      "Coffee with prospect",    7.20),
    ("2026-03-03", "software",  "JetBrains licence",      89.00),
    ("2026-03-18", "transport", "Train ticket — Tainan",  35.40),
]
existing = cursor.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
if existing == 0:
    cursor.executemany(
        "INSERT INTO expenses (spent_on, category, description, amount) VALUES (?, ?, ?, ?)",
        sample_rows,
    )
    conn.commit()
    print(f"Seeded {len(sample_rows)} sample rows.\n")
else:
    print(f"Database already has {existing} rows — skipping seed.\n")

# -------------------------------------------------------------------------
# 3. SELECT — three realistic questions, three queries.
# -------------------------------------------------------------------------
print("--- All March 2026 software expenses ---")
for date, description, amount in cursor.execute(
    "SELECT spent_on, description, amount FROM expenses "
    "WHERE category = ? AND spent_on LIKE ? ORDER BY spent_on",
    ("software", "2026-03-%"),
):
    print(f"  {date}  {description:<30} ${amount:>7.2f}")

# SUM() aggregates inside the database — faster than looping in Python.
total = cursor.execute(
    "SELECT SUM(amount) FROM expenses WHERE category = ? AND spent_on BETWEEN ? AND ?",
    ("transport", "2026-01-01", "2026-03-31"),
).fetchone()[0] or 0.0
print(f"\nQ1 transport total: ${total:.2f}")

# Top-1 by amount: the single most expensive item this year.
biggest = cursor.execute(
    "SELECT spent_on, category, description, amount FROM expenses "
    "WHERE spent_on LIKE ? ORDER BY amount DESC LIMIT 1",
    ("2026-%",),
).fetchone()
if biggest:
    date, category, description, amount = biggest
    print(f"Biggest expense of 2026: {date}  [{category}]  {description}  ${amount:.2f}")

# -------------------------------------------------------------------------
# 4. UPDATE + DELETE — fix a mistake and remove a duplicate.
#    Always SELECT the row first to confirm you're acting on the right one.
# -------------------------------------------------------------------------
# Create a mis-categorised row plus an accidental duplicate to demo the fix.
cursor.execute(
    "INSERT INTO expenses (spent_on, category, description, amount) VALUES (?, ?, ?, ?)",
    ("2026-05-10", "meal", "ChatGPT Plus subscription", 20.00),
)
wrong_id = cursor.lastrowid
cursor.execute(
    "INSERT INTO expenses (spent_on, category, description, amount) VALUES (?, ?, ?, ?)",
    ("2026-05-10", "meal", "ChatGPT Plus subscription", 20.00),
)
duplicate_id = cursor.lastrowid

print(f"\nFixing row #{wrong_id} (wrong category)...")
cursor.execute("UPDATE expenses SET category = ? WHERE id = ?", ("software", wrong_id))

print(f"Removing duplicate row #{duplicate_id}...")
cursor.execute("DELETE FROM expenses WHERE id = ?", (duplicate_id,))

# Without commit(), every change above is silently discarded when the
# connection closes. This is a feature: it lets us bundle related changes.
conn.commit()
conn.close()
print("Done. Inspect expenses.db with any SQLite viewer to verify.")
