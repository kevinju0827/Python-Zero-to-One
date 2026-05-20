import sqlite3

DATABASE = 'contacts.db'
DIVIDER = '-' * 55
HEADER  = '=' * 55


def setup_database():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                name    TEXT    NOT NULL,
                phone   TEXT,
                email   TEXT,
                note    TEXT
            )
        ''')

def add_contact(name, phone, email, note):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO contacts (name, phone, email, note) VALUES (?, ?, ?, ?)',
            (name, phone, email, note)
        )
        # cursor.lastrowid gives us the id the database assigned to the new row
        new_id = cursor.lastrowid

    print(f'\n  Contact "{name}" saved with ID {new_id}.')


def list_contacts():
    with sqlite3.connect(DATABASE) as connection:
        connection.row_factory = sqlite3.Row   # Enable dict-like row access
        cursor = connection.cursor()

        # ORDER BY name sorts the results alphabetically before returning them.
        # Sorting in the database is faster than sorting in Python for large datasets.
        cursor.execute('SELECT * FROM contacts ORDER BY name')
        contacts = cursor.fetchall()

    # We handle the "no data" case before trying to display anything
    if not contacts:
        print('\n  No contacts found. Add one first!')
        return

    print_contacts_table(contacts)
    print(f'\n  Total: {len(contacts)} contact(s)')

def search_contact(keyword):
    pattern = f'%{keyword}%'   # e.g., 'ali' becomes '%ali%'

    with sqlite3.connect(DATABASE) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # The LIKE comparison is case-insensitive by default in SQLite for ASCII text
        cursor.execute(
            'SELECT * FROM contacts WHERE name LIKE ? ORDER BY name',
            (pattern,)
        )
        results = cursor.fetchall()

    if not results:
        print(f'\n  No contacts found matching "{keyword}".')
        return

    print(f'\n  Search results for "{keyword}":')
    print_contacts_table(results)
    print(f'\n  Found: {len(results)} contact(s)')


def update_contact(contact_id, name, phone, email, note):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(
            '''
            UPDATE contacts
            SET name = ?, phone = ?, email = ?, note = ?
            WHERE id = ?
            ''',
            (name, phone, email, note, contact_id)
        )
        affected = cursor.rowcount

    if affected == 0:
        print(f'\n  No contact found with ID {contact_id}. Nothing was updated.')
    else:
        print(f'\n  Contact ID {contact_id} updated successfully.')


def delete_contact(contact_id):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
        affected = cursor.rowcount

    if affected == 0:
        print(f'\n  No contact found with ID {contact_id}. Nothing was deleted.')
    else:
        print(f'\n  Contact ID {contact_id} deleted.')


def print_contacts_table(contacts):
    print()
    print(f'  {"ID":<5} {"Name":<20} {"Phone":<15} {"Email":<25} {"Note"}')
    print(f'  {DIVIDER}')

    for row in contacts:
        # We use 'or ""' to handle None values gracefully.
        # If phone, email, or note was not provided, None becomes an empty string.
        contact_id = row['id']
        name       = row['name']       or ''
        phone      = row['phone']      or ''
        email      = row['email']      or ''
        note       = row['note']       or ''

        # Truncate long values so the table stays aligned
        print(f'  {contact_id:<5} {name:<20} {phone:<15} {email:<25} {note[:20]}')


def print_single_contact(contact):
    print()
    print(f'  ID    : {contact["id"]}')
    print(f'  Name  : {contact["name"]  or "(not set)"}')
    print(f'  Phone : {contact["phone"] or "(not set)"}')
    print(f'  Email : {contact["email"] or "(not set)"}')
    print(f'  Note  : {contact["note"]  or "(not set)"}')
    print()


def prompt(label, required=False):
    while True:
        value = input(f'  {label}: ').strip()
        if value:
            return value
        if not required:
            return None
        print('  This field is required. Please enter a value.')


def prompt_int(label):
    while True:
        raw = input(f'  {label}: ').strip()
        try:
            return int(raw)
        except ValueError:
            print('  Please enter a valid number.')


def handle_add():
    print(f'\n--- Add New Contact {DIVIDER[19:]}')
    name  = prompt('Name (required)', required=True)
    phone = prompt('Phone')
    email = prompt('Email')
    note  = prompt('Note')
    add_contact(name, phone, email, note)


def handle_list():
    print(f'\n--- All Contacts {DIVIDER[16:]}')
    list_contacts()


def handle_search():
    print(f'\n--- Search Contacts {DIVIDER[19:]}')
    keyword = prompt('Search by name', required=True)
    search_contact(keyword)


def handle_update():
    print(f'\n--- Update Contact {DIVIDER[18:]}')

    contact_id = prompt_int('Enter the ID of the contact to update')

    # First, show the current details so the user knows what they are changing
    with sqlite3.connect(DATABASE) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
        existing = cursor.fetchone()

    if existing is None:
        print(f'\n  No contact found with ID {contact_id}.')
        return

    print('\n  Current details:')
    print_single_contact(existing)
    print('  Enter new values (press Enter to keep the current value):')

    # Pre-fill the prompts with the existing value as a hint
    name  = input(f'  Name  [{existing["name"]}]: ').strip()  or existing['name']
    phone = input(f'  Phone [{existing["phone"] or ""}]: ').strip() or existing['phone']
    email = input(f'  Email [{existing["email"] or ""}]: ').strip() or existing['email']
    note  = input(f'  Note  [{existing["note"]  or ""}]: ').strip() or existing['note']

    update_contact(contact_id, name, phone, email, note)


def handle_delete():
    print(f'\n--- Delete Contact {DIVIDER[18:]}')

    contact_id = prompt_int('Enter the ID of the contact to delete')

    # Show the contact first and ask for confirmation
    with sqlite3.connect(DATABASE) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
        existing = cursor.fetchone()

    if existing is None:
        print(f'\n  No contact found with ID {contact_id}.')
        return

    print('\n  You are about to delete:')
    print_single_contact(existing)
    confirm = input('  Are you sure? Type "yes" to confirm: ').strip().lower()

    if confirm == 'yes':
        delete_contact(contact_id)
    else:
        print('\n  Deletion cancelled.')


def main():
    # Run silently on startup — creates the .db file and table if needed
    setup_database()

    print(HEADER)
    print('         Welcome to your Contact Book')
    print(HEADER)

    # Map each menu number to its handler function.
    # Using a dictionary avoids a long chain of if/elif blocks.
    menu_options = {
        '1': ('List all contacts',    handle_list),
        '2': ('Add a contact',        handle_add),
        '3': ('Search by name',       handle_search),
        '4': ('Update a contact',     handle_update),
        '5': ('Delete a contact',     handle_delete),
    }

    while True:
        print(f'\n{HEADER}')
        for key, (label, _) in menu_options.items():
            print(f'  {key}. {label}')
        print(f'  6. Quit')
        print(HEADER)

        choice = input('  Enter your choice (1-6): ').strip()

        if choice == '6':
            print('\n  Goodbye!\n')
            break

        if choice in menu_options:
            label, handler = menu_options[choice]
            try:
                handler()
            except sqlite3.Error as err:
                # Catch any unexpected database error so the program doesn't crash
                print(f'\n  Database error: {err}')
                print('  Please try again.')
        else:
            print('\n  Invalid choice. Please enter a number from 1 to 6.')


if __name__ == '__main__':
    main()