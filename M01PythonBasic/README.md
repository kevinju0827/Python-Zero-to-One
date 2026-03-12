# M01 Python Basic

## The "Why?"

In real life, you'll often run into repetitive tasks—renaming hundreds of photos, downloading files from dozens of websites, crunching large datasets, or repeating the same reporting steps every day.  
This is where programming shines: spending just ten minutes writing a small script can let your computer handle work that would otherwise take hours.  
Once automated, a workflow becomes repeatable, scalable, and less error-prone.  
Python is especially well-suited for these tasks because it is easy to read and write, has a huge ecosystem of libraries, and works great for automation, data processing, and quick prototyping.

## Goals

Understand what Python is and how to get started with Python and vibe coding (AI-assisted development).

## Core Concepts

### Interactive mode

Unlike many programming languages (such as C, C#, Go, and Java), Python is an interpreted language.  
In most cases, you don't need a separate compiler toolchain to see results.  
You simply write a script and run it to execute, and you'll immediately see the results.  
This is most easily demonstrated through Python's interactive mode, which you can treat like a "calculator + mini lab" for experimenting with ideas, testing syntax, and doing quick computations.

You can use Python's interactive mode to solve simple math problems.  
For example, to calculate `123 + 777`, type `123 + 777` and press Enter.

Common math operators in Python:

- Addition: `3 + 2` → `5`
- Subtraction: `10 - 4` → `6`
- Multiplication: `6 * 7` → `42`
- Division: `8 / 2` → `4.0`

  You can also try these useful operators:

- Floor division: `7 // 2` → `3`
- Modulus (remainder): `7 % 2` → `1`
- Power: `2 ** 3` → `8`

### Python Script

To avoid entering the same commands repeatedly, we can create a Python script.  
Once written, you can run the script again in the future without retyping the commands.

Create a new file named `hello.py` and paste the following code:

```python
print("Hello, world!")
```

Run the script by entering `python hello.py` in the terminal.  
This will display `Hello, world!` in the console.

The `print()` function is used to display text or other data in the console.  
It is a fundamental tool for debugging and communication in Python development.

### Vibe coding

Vibe coding is a practical workflow for building software with AI as a collaborator.  
You provide goals, constraints, context, and examples; the AI produces a draft solution; then you run it, observe the results, and iterate with feedback until it works reliably.  
Python is a great match for vibe coding because it runs quickly, is straightforward to read, and provides immediate feedback.  
AI can also help generate and work with Python scripts directly, making it useful for tasks such as complex calculations and operating system automation.

> Reminder: AI is excellent at producing a first draft and exploring options, but it does not guarantee correctness. Your job is not to trust it—your job is to verify it.

## Guided Practice

* Step 1: Open Python interactive mode  
  Open Python's interactive mode by clicking the Python app or by typing `python` in your terminal.  
  If you are using PyCharm, click the Python Console icon at the bottom left.  
  You will see the Python version and a prompt like `>>>`, indicating that you are in interactive mode.

* Step 2: Calculate a math problem  
  Assume your height is `1.75` meters and your weight is `70` kilograms.  
  To calculate your BMI, type `70 / 1.75 / 1.75` and press Enter.  
  Use a calculator to double-check that the answer is correct.

* Step 3: Save the calculation as a script  
  Create a new script file named `bmi.py` and paste the following code: `print(70 / 1.75 / 1.75)`
  Run the script by entering `python bmi.py` in the terminal.  
  This will display the BMI result in the console.


## Checkpoints

* [ ] Use Python to solve the following problem:  
      Let's say you are 20 years old and currently have 100,000 in savings.  
      If you invest this money in an index fund with an annual return of 5% and reinvest the gains,  
      how much will you have when you retire at 60 (40 years from now)?  
      (Hint: `x ** y` can be used for power calculations.)
