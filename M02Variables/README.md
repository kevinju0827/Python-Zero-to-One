# M02 Variables & Types

![Module 2 of 16](https://img.shields.io/badge/Module-2_of_16-6366f1?style=flat-square)
![Beginner](https://img.shields.io/badge/Difficulty-Beginner-4ade80?style=flat-square)
![~1 hour](https://img.shields.io/badge/Time-~1_hour-60a5fa?style=flat-square)
![Prerequisites: M01 — print() & math](https://img.shields.io/badge/Prerequisites-M01:_print()_%26_math-94a3b8?style=flat-square)

**Topics covered:** variables · `str` / `int` / `float` / `bool` · type conversion · string methods · f-strings · `input()`

## The Why?

In M01, we ran calculations directly —`70 / 1.75 / 1.75` —which works for a one-off calculation.
But what if you need to reuse that result? Or write a script that calculates the BMI for *any* person, not just someone who is exactly 1.75 m and 70 kg?

**Variables** are the answer. They are labeled storage boxes that hold a value so you can name it, reuse it, and change it later. Combined with **string operations** (for working with text) and **user input** (for making scripts interactive), variables transform your programs from static calculators into flexible, reusable tools.

---

## Core Concepts

### Variables —Named Storage

Use the `=` operator to store a value in a variable:

```python
weight = 70
height = 1.75
bmi = weight / height / height
print(bmi)   # 22.857...
```

**Naming rules:**
- Use descriptive names: `user_age` beats `x`
- Letters, numbers, underscores only —no spaces
- Cannot start with a number: `2score` is invalid, `score2` is fine
- Python convention: `snake_case` (words joined by underscores)

You can reassign a variable at any time —the new value replaces the old one:

```python
score = 85
score = score + 5   # Now 90
```

---

### Data Types

Every value in Python has a **type**. The four primitive types you will use constantly:

| Type | Example | What it stores |
|------|---------|---------------|
| `int` | `42`, `-7` | Whole numbers |
| `float` | `3.14`, `-0.5` | Decimal numbers |
| `str` | `"hello"`, `'world'` | Text (always in quotes) |
| `bool` | `True`, `False` | Yes/No, on/off values |

Check the type of any value with `type()`:

```python
print(type(42))       # <class 'int'>
print(type("hello"))  # <class 'str'>
print(type(3.14))     # <class 'float'>
```

---

### Type Conversion

Python will not automatically mix types in calculations. You must convert explicitly:

```python
age_text = "25"          # This is a string
age_number = int(age_text)   # Convert to integer
print(age_number + 1)    # 26
```

| Function | Converts to | Example |
|----------|-------------|---------|
| `int(x)` | Integer | `int("42")` —`42` |
| `float(x)` | Float | `float("3.14")` —`3.14` |
| `str(x)` | String | `str(100)` —`"100"` |
| `bool(x)` | Boolean | `bool(0)` —`False`, `bool(1)` —`True` |

> **Common mistake:** `input()` always returns a string, even if the user types a number. Always convert before doing math (see below).

---

### String Operations

Text in Python is called a **string** (`str`). Strings go inside single or double quotes —both work.

**Concatenation** —join strings with `+`:

```python
first = "Hello"
last  = "World"
print(first + ", " + last + "!")   # Hello, World!
```

**f-strings** —the cleanest way to embed variables inside text:

```python
name = "Alice"
score = 95.5
print(f"Name: {name}, Score: {score:.1f}")   # Name: Alice, Score: 95.5
```

The `f` before the opening quote activates f-string mode. Anything inside `{}` is evaluated as Python code.

**Useful string methods:**

```python
message = "  Hello, World!  "
print(message.upper())     # "  HELLO, WORLD!  "
print(message.lower())     # "  hello, world!  "
print(message.strip())     # "Hello, World!"  —removes leading/trailing spaces
print(message.replace("World", "Python"))  # "  Hello, Python!  "
print(len(message))        # 18  —total character count including spaces
```

---

### User Input —Making Scripts Interactive

`input()` pauses your script and waits for the user to type something, then returns it as a string:

```python
name = input("What is your name? ")
print(f"Nice to meet you, {name}!")
```

Since `input()` always returns a string, **convert before doing math:**

```python
age_str = input("Enter your age: ")
age     = int(age_str)          # Convert string —int
print(f"Next year you will be {age + 1}.")
```

Or inline:

```python
weight = float(input("Weight (kg): "))
height = float(input("Height (m): "))
bmi    = weight / height / height
print(f"Your BMI is {bmi:.2f}")
```

The `:.2f` inside `{}` is a **format spec** —it rounds the float to 2 decimal places.

---

## Going Further

<details>
<summary>Advanced f-string Formatting</summary>

```python
price = 12345.678
print(f"{price:,.2f}")    # 12,345.68  —comma separator + 2 decimal places
print(f"{price:>15.2f}")  # right-align in a 15-char wide column
print(f"{'Label':<10}")   # left-align in a 10-char wide column
```

</details>

<details>
<summary>Multi-line Strings</summary>

Use triple quotes for strings that span multiple lines:

```python
message = """
Dear Alice,
Your score is 95.
Congratulations!
"""
print(message)
```

</details>

<details>
<summary>The `None` Type</summary>

`None` is Python's way of saying "no value". Variables default to `None` if not initialized:

```python
result = None
print(type(result))   # <class 'NoneType'>
```

You will see `None` often when a function does not explicitly return anything.

</details>

<details>
<summary>Type Errors Are Your Friends</summary>

When Python raises a `TypeError` or `ValueError`, it is telling you exactly where a type mismatch occurred. Read the message:

```
ValueError: could not convert string to float: 'abc'
```

This tells you: `float("abc")` failed because `"abc"` is not a number. Fix: validate the input before converting (covered in M08).

</details>

<details>
<summary>Asking AI About Variables</summary>

When AI generates code that uses variable names you do not recognize, ask:
- *"What does the variable `response_data` contain at this point?"*
- *"Why is this value a string instead of a number?"*
- *"Rewrite this using descriptive variable names so I can understand each step."*

</details>

---

## Guided Practice

**Scenario:** A gym instructor wants a quick tool to check any member's BMI on the spot. The script should ask for their name, weight, and height, then display a personalized, formatted result. We will build an **interactive BMI calculator** that accepts any person's measurements and produces a clean output.

### Step 1 —Collect inputs

Create a new file `dynamic_bmi_example.py`.
Ask the user for their name, weight, and height. Convert the numeric inputs to floats:

```python
name   = input("Enter your name: ")
weight = float(input("Enter weight (kg): "))
height = float(input("Enter height (m): "))
```

### Step 2 —Calculate and format

Calculate BMI and store it in a variable. Use an f-string with `:.2f` to display two decimal places:

```python
bmi = weight / height / height
print(f"\n{name}'s BMI is {bmi:.2f}")
```

### Step 3 —Run and test

Run the script several times with different inputs. Verify the calculation matches an online BMI calculator.

### Step 4 —Extend with AI

Ask your AI assistant:

> "Extend this Python script to also display the BMI category: Underweight (<18.5), Normal (18.5–24.9), Overweight (25–29.9), Obese (≥30). Keep the same `input()` structure I already have."

Paste the response, run it, and verify each category prints correctly for different inputs.

---

## Checkpoints

* [ ] **Currency Converter**
  Ask the user to enter an amount in USD.
  Create a variable for the exchange rate (e.g., `exchange_rate = 31.5`).
  Calculate the equivalent in TWD and print:
  `100.00 USD = 3150.00 TWD`
  *(Hint: use `:.2f` in your f-string to show two decimal places for both values.)*

* [ ] **Age Calculator**
  Ask the user for their birth year.
  Store the current year in a variable (e.g., `current_year = 2026`).
  Calculate their age and print: `"You are turning 26 this year!"`
  *(Bonus: what happens if the user types their name instead of a number? Try it —we will fix crashes like this in M08.)*

* [ ] **Receipt Printer**
  A café sells coffee ($80), cake ($150), and juice ($65).
  Ask the user how many of each item they want.
  Calculate the subtotal, apply a 10% service charge, and print a formatted receipt:
  ```
  === Receipt ===
  Coffee × 2 :  $160
  Cake   × 1 :  $150
  Juice  × 0 :    $0
  ──────────────────
  Subtotal   :  $310
  Service 10%:   $31
  Total      :  $341
  ```
