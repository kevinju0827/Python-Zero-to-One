# M01 Python Basic

![Module 1 of 16](https://img.shields.io/badge/Module-1_of_16-6366f1?style=flat-square)
![Beginner](https://img.shields.io/badge/Difficulty-Beginner-4ade80?style=flat-square)
![~1 hour](https://img.shields.io/badge/Time-~1_hour-60a5fa?style=flat-square)
![No Prerequisites](https://img.shields.io/badge/Prerequisites-None-94a3b8?style=flat-square)

**Topics covered:** interactive mode 繚 math operators 繚 `print()` 繚 Python scripts 繚 vibe coding workflow

## The Why?

Repetitive tasks eat your time: renaming hundreds of photos, downloading files from dozens of links, crunching spreadsheet data every morning, sending customized messages to a list of contacts. Writing a ten-minute script can replace hours of manual work ??and once it exists, you can run it again instantly, forever.

Python is the right language to start with because:
- It reads almost like plain English ??no semicolons, no type declarations, no compiler.
- It runs immediately: write a line, see the result.
- Its ecosystem covers automation, data analysis, web, AI, and more.
- AI assistants are exceptionally good at writing Python ??which is exactly the workflow we will use.

By the end of this module, you will have written and run your first Python scripts, and you will understand the **vibe coding** workflow that powers everything that follows.

---

## Core Concepts

### Interactive Mode ??Python as a Calculator

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

### Python Scripts ??Writing Code That Lasts

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

**`print()`** is the function you will use constantly ??it displays text, numbers, or any value in the console. It is the simplest way to see what your code is doing.

---

### Vibe Coding ??AI as a Collaborator

**Vibe coding** is a practical workflow for building software with AI as a partner:

```
You describe the goal
    ??AI writes a first draft
        ??You run it and observe
            ??You iterate with feedback
```

Python is ideal for this loop because it runs instantly and gives you immediate feedback.

> **The golden rule:** AI is excellent at producing a first draft, but it does not guarantee correctness. Your job is not to trust it ??your job is to **verify and fix it**. That is exactly what this course teaches you to do.

A good vibe-coding prompt is specific:
- ??"Write a Python script"
- ??"Write a Python script that asks the user for their height and weight, calculates their BMI, and prints the result rounded to 2 decimal places"

The more context you give, the better the first draft.

---

## Going Further

<details>
<summary>Order of Operations</summary>

Python follows standard math precedence (PEMDAS/BODMAS). Use parentheses to make your intent explicit:

```python
print(2 + 3 * 4)      # 14  (multiplication before addition)
print((2 + 3) * 4)    # 20  (parentheses first)
```

</details>

<details>
<summary>Integer vs. Float Division</summary>

```python
print(7 / 2)    # 3.5   ??always a float
print(7 // 2)   # 3     ??floor division, always an int
print(7 % 2)    # 1     ??remainder
```

The `%` operator is surprisingly useful: `n % 2 == 0` checks if `n` is even.

</details>

<details>
<summary>Running Scripts from the IDE</summary>

In PyCharm: right-click your `.py` file ??**Run**.
In VS Code: click the ??button at the top right.
Both show the output in a built-in terminal panel ??no need to switch windows.

</details>

<details>
<summary>AI Prompt Patterns for This Module</summary>

| Goal | Prompt template |
|------|----------------|
| Calculate something | "Write a Python one-liner that calculates [formula]" |
| Explain an operator | "Explain what `//` does in Python with an example" |
| Debug output | "This Python code prints [X] but I expected [Y]. Why?" |

</details>

---

## Guided Practice

### Step 1 ??Open interactive mode

Open your terminal (or PyCharm's **Python Console** at the bottom of the window).
You should see `>>>`.

### Step 2 ??Calculate a BMI

Your height is `1.75` m and weight is `70` kg.
The BMI formula is: `weight / height / height`

Type this and press Enter:

```python
70 / 1.75 / 1.75
```

Verify the answer with a calculator. You should get approximately `22.86`.

### Step 3 ??Save the calculation as a script

Create a new file named `bmi.py` and add:

```python
print(70 / 1.75 / 1.75)
```

Run it with:

```bash
python bmi.py
```

The result should print to the console.

### Step 4 ??Use AI to extend the script

Ask your AI assistant:

> "Extend this Python script so it asks the user for their height and weight, calculates their BMI, and prints a sentence like: `Your BMI is 22.86`"

Paste the response into a new file, run it, and verify it works. If it does not, copy the error message and ask the AI to fix it.

---

## Checkpoints

* [ ] **Compound Interest Calculator**
  You are 20 years old and have 瞼100,000 in savings.
  You invest in an index fund with a 5% annual return (compounding yearly).
  How much will you have when you retire at 60 (40 years from now)?
  *(Hint: the formula is `principal * (1 + rate) ** years`. The `**` operator handles the exponent.)*

* [ ] **Unit Converter**
  Use Python interactive mode (or a script) to:
  1. Convert `100` kilometres to miles (`? 0.6214`).
  2. Convert `37.5` degrees Celsius to Fahrenheit (`? 9/5 + 32`).
  3. Convert `1500` watts to horsepower (`/ 745.7`).
  Print each result.
