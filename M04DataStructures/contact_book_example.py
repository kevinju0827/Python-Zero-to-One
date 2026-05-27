contacts = [
    {"name": "Alice Chen",  "phone": "0912-111-222", "group": "work"},
    {"name": "Bob Wang",    "phone": "0923-333-444", "group": "family"},
    {"name": "Carol Lin",   "phone": "0934-555-666", "group": "work"},
]

# --- Display all contacts ---
print("=== All Contacts ===")
for contact in contacts:
    print(f"  {contact['name']:<15} | {contact['phone']} | {contact['group']}")

# --- Add a new contact ---
new_contact = {
    "name": "David Huang",
    "phone": "0945-777-888",
    "group": "family"
}
contacts.append(new_contact)
print(f"\nAdded '{new_contact['name']}'. Total contacts: {len(contacts)}")

# --- Search by name ---
search_term = input("\nSearch contact name: ").lower()

found = None
for contact in contacts:
    if search_term in contact["name"].lower():
        found = contact
        break

if found:
    print(f"Found: {found['name']} — {found['phone']} ({found['group']})")
else:
    print("No contact found.")

# --- Group summary using a set ---
groups = set(c["group"] for c in contacts)

print("\n=== Group Summary ===")
for group in sorted(groups):
    count = sum(1 for c in contacts if c["group"] == group)
    print(f"  {group}: {count} contact(s)")
