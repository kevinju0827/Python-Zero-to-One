# M07 Object-Oriented Programming

![Module 7 of 16](https://img.shields.io/badge/Module-7_of_16-6366f1?style=flat-square)
![Beginner](https://img.shields.io/badge/Difficulty-Beginner-4ade80?style=flat-square)
![1.5 hours](https://img.shields.io/badge/Time-1.5_hours-60a5fa?style=flat-square)
![Prerequisites: M06 — def & return](https://img.shields.io/badge/Prerequisites-M06:_def_%26_return-94a3b8?style=flat-square)

**Topics covered:** classes · `__init__` · instance attributes · methods · `self` · inheritance · `super()` · `__str__`

## The Why?

So far, your programs have been built from functions and data structures that sit independently of each other. As programs grow, keeping related data and the functions that operate on it in sync becomes fragile.

**Object-Oriented Programming (OOP)** solves this by bundling data and behaviour together into a single unit called a **class**. A class is a blueprint; an **object** (or instance) is the thing you actually create from that blueprint.

This matters for two practical reasons:

1. **AI-generated code uses classes everywhere.** FastAPI routes, PySide6 windows, database models, and data parsers all rely on classes. Without understanding them, you can run AI-generated code but you cannot read, modify, or debug it confidently.
2. **Real-world programs model real-world things.** A `BankAccount` with a `balance` and a `deposit()` method is far clearer than a loose dict and a stray function that happens to go with it.

---

## Core Concepts

### What Is a Class?

A class defines a new **type** of object —its data (attributes) and its behaviours (methods).

```
Pseudocode:
class ThingName:
    def __init__(self, initial_data):
        self.data = initial_data       —store data on the object

    def do_something(self):
        use self.data to do work
```

```python
class Dog:
    def __init__(self, name, breed):
        self.name  = name    # instance attribute
        self.breed = breed

    def bark(self):
        print(f"{self.name} says: Woof!")

# Create instances (objects) from the class
dog1 = Dog("Rex",   "Labrador")
dog2 = Dog("Bella", "Poodle")

dog1.bark()   # Rex says: Woof!
dog2.bark()   # Bella says: Woof!
```

Each object has its **own copy** of the attributes. Changing `dog1.name` does not affect `dog2`.

---

### `__init__` —The Constructor

`__init__` is called automatically every time you create a new object.
Use it to set the object's initial state.

```python
class BankAccount:
    def __init__(self, owner, initial_balance=0):
        self.owner   = owner
        self.balance = initial_balance

account = BankAccount("Alice", 1000)
print(account.balance)   # 1000
```

---

### `self` —Referring to the Current Object

`self` is the first parameter of every method. It refers to the specific instance the method was called on.
Python passes it automatically —you never supply it yourself when calling.

```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1    # self.count means THIS object's count

    def reset(self):
        self.count = 0

c = Counter()
c.increment()
c.increment()
print(c.count)   # 2
c.reset()
print(c.count)   # 0
```

---

### Methods —Functions That Belong to a Class

Any function defined inside a class is a **method**. Methods have access to the object's data through `self`.

```python
class BankAccount:
    def __init__(self, owner, initial_balance=0):
        self.owner   = owner
        self.balance = initial_balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        return self.balance

    def summary(self):
        print(f"Account: {self.owner} | Balance: ${self.balance:,.2f}")
```

---

### `__str__` —Human-Readable Representation

Define `__str__` to control what `print(object)` shows:

```python
class BankAccount:
    ...
    def __str__(self):
        return f"BankAccount({self.owner}, ${self.balance:,.2f})"

account = BankAccount("Alice", 500)
print(account)   # BankAccount(Alice, $500.00)
```

Without `__str__`, `print(account)` shows something like `<__main__.BankAccount object at 0x...>` —not useful.

---

### Inheritance —Reusing and Extending Classes

A **child class** inherits all attributes and methods from its **parent class**, and can add or override them.

```
Pseudocode:
class ChildClass(ParentClass):
    def __init__(self, ...):
        super().__init__(...)   —call the parent's __init__ first
        self.extra = value      —add child-specific attributes
```

```python
class SavingsAccount(BankAccount):
    def __init__(self, owner, initial_balance=0, interest_rate=0.02):
        super().__init__(owner, initial_balance)   # run BankAccount.__init__
        self.interest_rate = interest_rate

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        print(f"Interest added: ${interest:.2f}. New balance: ${self.balance:,.2f}")

savings = SavingsAccount("Bob", 5000, interest_rate=0.03)
savings.deposit(1000)       # inherited from BankAccount
savings.apply_interest()    # only on SavingsAccount
savings.summary()           # inherited from BankAccount
```

`super().__init__(...)` is required —without it, the parent's setup code never runs.

---

### When to Use a Class

```
Multiple functions share the same piece of state? —class
You need multiple independent instances of the same structure? —class
You're building something AI generated that uses classes? —understand it as-is
Simple script, no shared state, few functions? —plain functions are fine
```

---

## Going Further

<details>
<summary>Class vs. Instance Attributes</summary>

Attributes set directly on the class (outside `__init__`) are **shared** by all instances:

```python
class Dog:
    species = "Canis lupus familiaris"   # class attribute —shared

    def __init__(self, name):
        self.name = name                 # instance attribute —per object

d1 = Dog("Rex")
d2 = Dog("Bella")
print(d1.species)   # same for both
print(d1.name)      # Rex
print(d2.name)      # Bella
```

Use class attributes for data that is the same for every instance (constants, counters).

</details>

<details>
<summary>`@property` —Computed Attributes</summary>

Use `@property` to define a method that behaves like an attribute —no parentheses needed when accessing it:

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        import math
        return math.pi * self.radius ** 2

c = Circle(5)
print(c.area)   # 78.54...  —no () needed
```

This is common in AI-generated code —you will recognize it now.

</details>

<details>
<summary>`@staticmethod` and `@classmethod`</summary>

**`@staticmethod`** —a function that logically belongs to the class but does not need `self` or `cls`:

```python
class Temperature:
    @staticmethod
    def celsius_to_fahrenheit(c):
        return c * 9 / 5 + 32

print(Temperature.celsius_to_fahrenheit(100))   # 212.0
```

**`@classmethod`** —receives the class itself as `cls`, useful for alternative constructors:

```python
class BankAccount:
    @classmethod
    def from_dict(cls, data):
        return cls(data["owner"], data["balance"])

account = BankAccount.from_dict({"owner": "Alice", "balance": 500})
```

</details>

<details>
<summary>Dunder (Magic) Methods</summary>

Python uses double-underscore methods to define object behaviour for built-in operations:

| Method | Called when |
|--------|-------------|
| `__str__` | `print(obj)` or `str(obj)` |
| `__len__` | `len(obj)` |
| `__eq__` | `obj1 == obj2` |
| `__lt__` | `obj1 < obj2` (enables sorting) |
| `__add__` | `obj1 + obj2` |

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

v = Vector(1, 2) + Vector(3, 4)
print(v)   # Vector(4, 6)
```

</details>

<details>
<summary>Asking AI About Classes</summary>

When AI generates a class you do not understand, ask:
- *"Explain what `__init__` does in this class and why each attribute is stored on `self`."*
- *"What does `super().__init__()` do in this child class?"*
- *"Rewrite this code without inheritance so I can see what is being shared."*

</details>

---

## Guided Practice

**Scenario:** A small community library tracks check-outs on a whiteboard. You offer to replace it with a Python script that manages the book collection, shows which titles are in or out at a glance, and lets staff search by title or author. We will build a **library book tracker** using a `Book` class and a `Library` class.

### Step 1 —Define the `Book` class

Create `library_example.py`:

```python
class Book:
    def __init__(self, title, author, year):
        self.title     = title
        self.author    = author
        self.year      = year
        self.is_checked_out = False

    def checkout(self):
        if self.is_checked_out:
            print(f"'{self.title}' is already checked out.")
        else:
            self.is_checked_out = True
            print(f"Checked out: '{self.title}'")

    def return_book(self):
        self.is_checked_out = False
        print(f"Returned: '{self.title}'")

    def __str__(self):
        status = "OUT" if self.is_checked_out else "IN"
        return f"[{status}] {self.title} —{self.author} ({self.year})"
```

### Step 2 —Define the `Library` class

```python
class Library:
    def __init__(self, name):
        self.name  = name
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print(f"Added: '{book.title}'")

    def show_all(self):
        print(f"\n=== {self.name} ===")
        if not self.books:
            print("  No books.")
        for book in self.books:
            print(f"  {book}")

    def search(self, keyword):
        keyword = keyword.lower()
        results = [b for b in self.books if keyword in b.title.lower() or keyword in b.author.lower()]
        return results
```

### Step 3 —Use the classes together

```python
lib = Library("City Library")

lib.add_book(Book("Clean Code",          "Robert C. Martin", 2008))
lib.add_book(Book("The Pragmatic Programmer", "Hunt & Thomas", 1999))
lib.add_book(Book("Python Crash Course", "Eric Matthes",     2023))

lib.show_all()

lib.books[0].checkout()
lib.books[0].checkout()   # Should print "already checked out"
lib.show_all()

lib.books[0].return_book()
lib.show_all()
```

### Step 4 —Add search and extend with inheritance

```python
results = lib.search("python")
print(f"\nSearch 'python': {len(results)} result(s)")
for b in results:
    print(f"  {b}")
```

Now extend with an `EBook` that adds a `file_size_mb` attribute:

```python
class EBook(Book):
    def __init__(self, title, author, year, file_size_mb):
        super().__init__(title, author, year)
        self.file_size_mb = file_size_mb

    def __str__(self):
        base = super().__str__()
        return f"{base} [{self.file_size_mb} MB]"

lib.add_book(EBook("Automate the Boring Stuff", "Al Sweigart", 2019, 3.2))
lib.show_all()
```

---

## Checkpoints

* [ ] **Student Grade Book**
  Create a `Student` class with `name`, `scores` (list), and these methods:
  - `add_score(score)` —appends to the list
  - `average()` —returns the mean score
  - `grade()` —returns "A"/"B"/"C"/"D"/"F" based on the average
  - `__str__` —displays `"Alice: avg 87.5 (B)"`
  Create at least 3 students, add scores to each, and print a sorted class ranking (highest average first).

* [ ] **Bank Account System**
  Build a `BankAccount` class and a `SavingsAccount` child class (as shown in Core Concepts).
  Create two accounts and simulate:
  1. Deposit and withdraw operations on the regular account.
  2. Apply monthly interest twice on the savings account.
  3. Print a final summary for both accounts.
  Add a class attribute `transaction_count` that increments with every deposit or withdrawal across all instances, and print the total at the end.

* [ ] **Simple Task Manager**
  Create a `Task` class (`title`, `priority` as `"high"/"medium"/"low"`, `done` flag) and a `TaskList` class.
  `TaskList` methods: `add(task)`, `complete(title)`, `pending()` (returns incomplete tasks), `show()`.
  Build a loop-driven terminal menu: add task, complete task, view pending, quit.
