# M04 Data Structures

![Module 4 of 16](https://img.shields.io/badge/Module-4_of_16-6366f1?style=flat-square)
![Beginner](https://img.shields.io/badge/Difficulty-Beginner-4ade80?style=flat-square)
![1.5–2 hours](https://img.shields.io/badge/Time-1.5--2_hours-60a5fa?style=flat-square)
![Prerequisites: M03 — if / elif / else](https://img.shields.io/badge/Prerequisites-M03:_if_%2F_elif_%2F_else-94a3b8?style=flat-square)

**Topics covered:** list · tuple · dictionary (`dict`) · set · indexing · slicing · common methods · choosing the right structure

## The Why?

In previous modules, each variable held exactly one value: one name, one score, one temperature.
Real data is rarely a single value — it is a *collection*. A gradebook holds 30 scores. A shopping cart holds many items with prices. A user profile has a name, an email, and a list of purchase history.

By the end of this module, you will be able to store, access, and modify any collection of data, and choose the right tool for the job. This is also the foundation for the next module, M05, where you will loop through these collections automatically.

---

## Core Concepts

Python has four built-in collection types that cover nearly every case you will encounter:

| Structure | Ordered? | Mutable? | Unique? | Typical Use |
|-----------|----------|----------|---------|-------------|
| `list`    | —Yes   | —Yes   | —No   | Sequences of items that can change |
| `tuple`   | —Yes   | —No    | —No   | Fixed groups of related values |
| `dict`    | —Yes   | —Yes   | Keys only | Key–value lookups (like a real dictionary) |
| `set`     | —No    | —Yes   | —Yes  | Deduplicated collections, fast membership tests |


### List —An Ordered, Changeable Sequence

A list stores multiple values in a fixed order inside square brackets `[]`.
You can add, remove, or change items at any time.

```python
# Creating a list
fruits = ["apple", "banana", "cherry"]

# Accessing by index (counting starts at 0)
print(fruits[0])   # apple
print(fruits[-1])  # cherry  —negative index counts from the end
```

**Slicing** extracts a sub-list:

```python
scores = [88, 72, 95, 60, 80]
top_three = scores[0:3]   # [88, 72, 95]  (index 0, 1, 2 —stop is excluded)
```

**Common list methods:**

```python
fruits.append("mango")       # Add to the end
fruits.insert(1, "blueberry") # Insert at position 1
fruits.remove("banana")       # Remove first match
popped = fruits.pop()         # Remove & return the last item
fruits.sort()                 # Sort in place (alphabetically or numerically)
print(len(fruits))            # Number of items
```

**Checking membership:**

```python
if "apple" in fruits:
    print("We have apples!")
```

---

### Tuple —An Ordered, Immutable Sequence

A tuple looks like a list but uses parentheses `()` and **cannot be changed** after creation.
Use tuples for data that should stay fixed: GPS coordinates, RGB colors, database rows.

```python
location = (25.0330, 121.5654)   # (latitude, longitude) —never changes
color    = (255, 165, 0)          # Orange in RGB

print(location[0])   # 25.033  —indexing works the same as lists
```

Trying to change a tuple raises an error:

```python
location[0] = 0   # —TypeError: 'tuple' object does not support item assignment
```

**Tuple unpacking** —a clean way to assign each element to a separate variable:

```python
lat, lon = location
print(f"Latitude: {lat}, Longitude: {lon}")
```

---

### Dictionary (`dict`) —Key-Value Lookup

A dictionary stores data as **key: value** pairs inside curly braces `{}`.
Think of it like a real dictionary: you look up a *word* (key) to find its *definition* (value).

```python
student = {
    "name": "Alice",
    "age": 20,
    "gpa": 3.8
}

# Access by key
print(student["name"])       # Alice

# Add or update a key
student["major"] = "CS"      # New key
student["gpa"]   = 3.9       # Update existing key

# Safe access —returns None if key doesn't exist (no crash)
grade = student.get("grade", "N/A")
```

**Common dict methods:**

```python
print(student.keys())    # All keys
print(student.values())  # All values
print(student.items())   # All key-value pairs (as tuples)

del student["age"]       # Remove a key
"name" in student        # True —membership test checks keys
```

**List of dicts** —the most common pattern you will see in real data (CSV rows, API responses):

```python
contacts = [
    {"name": "Alice", "phone": "0912-345-678"},
    {"name": "Bob",   "phone": "0987-654-321"},
]
print(contacts[0]["name"])   # Alice
```

---

### Set —A Bag of Unique Items

A set stores items without duplicates and without any guaranteed order.
Its main strengths: **automatic deduplication** and **fast `in` checks**.

```python
tags = {"python", "beginner", "automation"}
tags.add("python")    # Duplicate —silently ignored
print(tags)           # {'python', 'beginner', 'automation'}  (order may vary)

# Deduplication trick
raw = [3, 1, 4, 1, 5, 9, 2, 6, 5]
unique = set(raw)     # {1, 2, 3, 4, 5, 6, 9}
```

**Set operations** mirror math notation:

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a | b)   # Union:        {1, 2, 3, 4, 5, 6}
print(a & b)   # Intersection: {3, 4}
print(a - b)   # Difference:   {1, 2}
```

---

### Choosing the Right Structure

```
Need order AND the ability to change items?  —list
Need order but the data should never change? —tuple
Need to look things up by a name/label?      —dict
Need to store unique items / test membership fast? —set
```

---

## Going Further

<details>
<summary>Nested Structures</summary>

Real API responses and config files contain deeply nested data:

```python
user = {
    "name": "Alice",
    "address": {
        "city": "Taipei",
        "zip": "100"
    },
    "scores": [95, 87, 92]
}

print(user["address"]["city"])   # Taipei
print(user["scores"][1])         # 87
```

</details>

<details>
<summary>`defaultdict` for Cleaner Grouping</summary>

The `collections` module's `defaultdict` removes the need to check whether a key already exists:

```python
from collections import defaultdict

groups = defaultdict(list)
for c in contacts:
    groups[c["group"]].append(c["name"])

print(dict(groups))
# {'work': ['Alice Chen', 'Carol Lin'], 'family': ['Bob Wang', 'David Huang']}
```

</details>

<details>
<summary>List Comprehensions —A Pythonic Shortcut</summary>

Instead of a `for` loop + `append`, Python has a one-line syntax:

```python
work_contacts = [c["name"] for c in contacts if c["group"] == "work"]
```

This is called a **list comprehension**. You will see it everywhere in Python code.

</details>

<details>
<summary>Asking AI About Data Structures</summary>

When you ask an AI assistant to write code that manages data, the AI will almost always use dicts or lists. Understanding these structures lets you:
- Read and understand the generated code
- Spot when the AI chose the wrong structure (e.g., a list when a dict would make lookups faster)
- Ask follow-up questions like: *"Can you refactor this list of tuples into a list of dicts so I can access fields by name?"*

</details>

<details>
<summary>Performance: Set vs. List for `in` Checks</summary>

Checking `x in my_list` scans every element —O(n).
Checking `x in my_set` uses a hash table —O(1), regardless of size.
For 1,000+ items where you check membership often, convert to a set first.

</details>

---

## Guided Practice

**Scenario:** You manage a small project team and need a quick way to look up phone numbers from the terminal — without opening your phone or scrolling through a spreadsheet. We will build a **simple contact book** that stores contacts as a list of dicts, supports search by name, and prints a group summary.

### Step 1: Create the data structure

Create a new file `contact_book_example.py`.
Define a list of dictionaries, each representing one contact:

```python
contacts = [
    {"name": "Alice Chen",  "phone": "0912-111-222", "group": "work"},
    {"name": "Bob Wang",    "phone": "0923-333-444", "group": "family"},
    {"name": "Carol Lin",   "phone": "0934-555-666", "group": "work"},
]
```

### Step 2: Print all contacts

Loop through the list (we will cover loops fully in M05, but a preview helps here) and print each contact's details using an f-string:

```python
print("=== All Contacts ===")
for contact in contacts:
    print(f"  {contact['name']:<15} | {contact['phone']} | {contact['group']}")
```

Run the script. You should see all three contacts formatted neatly.

### Step 3: Add a new contact

Append a new dict to the list using `.append()`, then print the updated count:

```python
new_contact = {
    "name": "David Huang",
    "phone": "0945-777-888",
    "group": "family"
}
contacts.append(new_contact)
print(f"\nAdded '{new_contact['name']}'. Total contacts: {len(contacts)}")
```

### Step 4: Search by name

Ask the user for a name and scan the list to find a match:

```python
search_term = input("\nSearch contact name: ").lower()

found = None
for contact in contacts:
    if search_term in contact["name"].lower():
        found = contact
        break

if found:
    print(f"Found: {found['name']} —{found['phone']} ({found['group']})")
else:
    print("No contact found.")
```

### Step 5: Show group summary using a set

Use a set to collect all unique group names, then count how many contacts belong to each:

```python
groups = set(c["group"] for c in contacts)

print("\n=== Group Summary ===")
for group in groups:
    count = sum(1 for c in contacts if c["group"] == group)
    print(f"  {group}: {count} contact(s)")
```

Run the final script. You now have a working contact book that demonstrates all four data structures in one coherent program.

---

## Checkpoints

* [ ] **Playlist Manager**
  Build a script that manages a music playlist. Store songs as a list of dicts with `title`, `artist`, and `duration_seconds` keys. Your script should:
  1. Display all songs with their index number (1-based).
  2. Let the user input a song title to remove it from the playlist.
  3. Print the total playlist duration in `mm:ss` format.
  *(Hint: use `.remove()` carefully —it removes the first matching item. You may need to find the dict by title first.)*

* [ ] **Word Frequency Counter**
  Take a sentence string (hardcode one with repeated words, or ask the user for input).
  Split it into a list of words (`.split()`), convert to lowercase, and use a dict to count how many times each word appears.
  Print the top 3 most frequent words.
  *(Hint: `dict.get(word, 0) + 1` lets you increment a count without checking if the key exists first.)*

* [ ] **Unique Visitor Tracker**
  You run a small website and your server logs repeat visitor IPs. Given a list like:
  ```python
  visits = ["192.168.1.1", "10.0.0.2", "192.168.1.1", "172.16.0.5", "10.0.0.2", "10.0.0.2"]
  ```
  Use a set to find how many *unique* visitors you had.
  Then use a dict to count how many times each IP visited.
  Print a sorted report: most visits first.
