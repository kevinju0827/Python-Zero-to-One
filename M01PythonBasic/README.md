# M01 Python Basic

![Module 1 of 16](https://img.shields.io/badge/Module-1_of_16-6366f1?style=flat-square)
![Beginner](https://img.shields.io/badge/Difficulty-Beginner-4ade80?style=flat-square)
![~1 hour](https://img.shields.io/badge/Time-~1_hour-60a5fa?style=flat-square)
![No Prerequisites](https://img.shields.io/badge/Prerequisites-None-94a3b8?style=flat-square)

**Topics covered:** interactive mode · math operators · `print()` · Python scripts · vibe coding workflow

## The Why?

Repetitive tasks eat your time: renaming hundreds of photos, downloading files from dozens of links, crunching spreadsheet data every morning, sending customized messages to a list of contacts. Writing a ten-minute script can replace hours of manual work —and once it exists, you can run it again instantly, forever.

Python is the right language to start with because:
- It reads almost like plain English — no semicolons, no type declarations, no compiler.
- It runs immediately: write a line, see the result.
- Its ecosystem covers automation, data analysis, web, AI, and more.
- AI assistants are exceptionally good at writing Python — which is exactly the workflow we will use.

By the end of this module, you will have written and run your first Python scripts, and you will understand the **vibe coding** workflow that powers everything that follows.

---

## Core Concepts

### Interactive Mode — Python as a Calculator

Python is an **interpreted language**. Unlike C or Java, there is no separate compile step. You can type a line and see the result immediately.

The easiest way to try this is **interactive mode**: open a terminal and type `python` (or `python3` on macOS/Linux). You will see a `>>>` prompt.

```
>>> 123 + 777
900
>>> 2 ** 10
1024
```

Think of it as a smart calculator that also understands logic, text, and files.

**Common math operators:**

| Operator | Example | Result | Meaning |
|----------|---------|--------|---------|
| `+` | `3 + 2` | `5` | Addition |
| `-` | `10 - 4` | `6` | Subtraction |
| `*` | `6 * 7` | `42` | Multiplication |
| `/` | `8 / 2` | `4.0` | Division (always returns a decimal) |
| `//` | `7 // 2` | `3` | Floor division (drops the remainder) |
| `%` | `7 % 2` | `1` | Modulus (remainder only) |
| `**` | `2 ** 8` | `256` | Power / exponentiation |

> Exit interactive mode with `exit()` or `Ctrl+Z` (Windows) / `Ctrl+D` (macOS/Linux).

---

### Python Scripts — Writing Code That Lasts

Interactive mode is great for experiments, but you lose everything when you close the terminal.
A **Python script** is a plain text file ending in `.py` that Python runs from top to bottom.

Create a file named `hello.py` with this content:

```python
print("Hello, world!")
```

Run it from your terminal:

```bash
python hello.py
```

You should see:

```
Hello, world!
```

**`print()`** is the function you will use constantly — it displays text, numbers, or any value in the console. It is the simplest way to see what your code is doing.

---

### Vibe Coding — AI as a Collaborator

**Vibe coding** is a practical workflow for building software with AI as a partner:

```
You describe the goal
    — AI writes a first draft
        — You run it and observe
            — You iterate with feedback
```

Python is ideal for this loop because it runs instantly and gives you immediate feedback.

> **The golden rule:** AI is excellent at producing a first draft, but it does not guarantee correctness. Your job is not to trust it —your job is to **verify and fix it**. That is exactly what this course teaches you to do.

A good vibe-coding prompt is specific:
- ❌ "Write a Python script"
- ✅ "Write a Python script that asks the user for their height and weight, calculates their BMI, and prints the result rounded to 2 decimal places"

The more context you give, the better the first draft.

---

## Going Further

<details>
<summary>Order of Operations — When Precedence Causes Real Bugs</summary>

Python follows PEMDAS/BODMAS. This catches beginners more often than you expect:

```python
# Trying to average two exam scores
score_a, score_b = 80, 90
wrong = score_a + score_b / 2   # 125.0 — divides score_b first, then adds
right = (score_a + score_b) / 2 # 85.0  — correct

# Compound interest: the ** must come last
principal, rate, years = 10000, 0.05, 10
wrong = principal * 1 + rate ** years  # not what you want
right = principal * (1 + rate) ** years # 16288.95
```

**Rule of thumb:** if a formula has more than two operations, add parentheses even when you think they are not needed. They cost nothing and prevent bugs.

</details>

<details>
<summary>Integer vs. Float Division — and `round()`</summary>

```python
print(7 / 2)    # 3.5  — true division, always returns float
print(7 // 2)   # 3    — floor division, drops the remainder
print(7 % 2)    # 1    — remainder only (modulus)
```

`%` is more useful than it looks. Common patterns:

```python
# Is a number even?
print(10 % 2 == 0)   # True
print(7  % 2 == 0)   # False

# Does a number divide evenly?
print(100 % 25 == 0) # True — 100 is divisible by 25
```

Use `round()` to control decimal places in output:

```python
print(round(3.14159, 2))      # 3.14
print(round(7 / 3, 4))        # 2.3333
```

</details>

<details>
<summary>Reading Your First Error Message</summary>

You will see red text in the terminal. Do not panic — Python is telling you exactly what went wrong.

Every error has the same structure:

```
Traceback (most recent call last):
  File "bmi.py", line 3, in <module>
    print(weight / height / height)
          ^^^^^^
NameError: name 'weight' is not defined
```

| Part | What it means |
|------|--------------|
| `File "bmi.py", line 3` | Which file and which line caused the crash |
| `^^^^^^` | The specific expression Python could not evaluate |
| `NameError` | The category of error |
| `name 'weight' is not defined` | The specific cause |

**The three errors you will hit most often this week:**

| Error | Typical cause |
|-------|--------------|
| `SyntaxError` | Typo, missing colon, mismatched bracket |
| `NameError` | Used a variable before assigning it |
| `TypeError` | Mixed incompatible types (e.g., adding a number to a string) |

**Workflow:** read the last line of the traceback first. If it is unclear, paste the full error into your AI assistant and ask *"What caused this and how do I fix it?"*

</details>

<details>
<summary>AI Prompt Patterns for This Module</summary>

| Goal | Prompt template |
|------|----------------|
| Calculate something | `"Write a Python one-liner that calculates [formula]. Show the result with print()."` |
| Explain an operator | `"Explain what // does in Python. Show two examples where the result is different from /."` |
| Debug a wrong result | `"This Python code prints [X] but I expected [Y]. Here is my code: [paste]. What is wrong?"` |
| Explain an error | `"My Python script shows this error: [paste full traceback]. What caused it and how do I fix it?"` |
| Extend a script | `"Here is my script: [paste]. Extend it to also [new requirement]. Keep the same structure."` |

</details>

---

## Guided Practice

**Scenario:** You want to quickly check your own BMI and then hand a working script to a friend who can run it themselves — no app downloads, no spreadsheets, just Python. We will build a **BMI calculator** in two stages — first exploring in interactive mode, then saving it as a reusable script.

### Step 1 —Open interactive mode

Open your terminal (or PyCharm's **Python Console** at the bottom of the window).
You should see `>>>`.

### Step 2 —Calculate a BMI

Your height is `1.75` m and weight is `70` kg.
The BMI formula is: `weight / height / height`

Type this and press Enter:

```python
70 / 1.75 / 1.75
```

Verify the answer with a calculator. You should get approximately `22.86`.

### Step 3 —Save the calculation as a script

Create a new file named `bmi.py` and add:

```python
print(70 / 1.75 / 1.75)
```

Run it with:

```bash
python bmi.py
```

The result should print to the console.

### Step 4 —Use AI to extend the script

Ask your AI assistant:

> "Extend this Python script so it asks the user for their height and weight, calculates their BMI, and prints a sentence like: `Your BMI is 22.86`"

Paste the response into a new file, run it, and verify it works. If it does not, copy the error message and ask the AI to fix it.

---

## Checkpoints

* [ ] **Compound Interest Calculator**
  You are 20 years old and have $100,000 in savings.
  You invest in an index fund with a 5% annual return (compounding yearly).
  How much will you have when you retire at 60 (40 years from now)?
  *(Hint: the formula is `principal * (1 + rate) ** years`. The `**` operator handles the exponent.)*

* [ ] **Unit Converter**
  Use Python interactive mode (or a script) to:
  1. Convert `100` kilometres to miles (`× 0.6214`).
  2. Convert `37.5` degrees Celsius to Fahrenheit (`× 9/5 + 32`).
  3. Convert `1500` watts to horsepower (`/ 745.7`).
  Print each result.
