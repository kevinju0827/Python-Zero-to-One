# M02 Variables

## The "Why?"

In the previous module, we used Python as a powerful calculator.  
But what if you need to reuse a calculation result later?  
Or what if you want to write a script that calculates the BMI for *anyone*, not just someone who is exactly 1.75m tall and 70kg?  
This is where variables and inputs come in.  
Variables act like labeled storage boxes for your data, allowing you to save information and reuse it without retyping it.  
By combining variables with string (text) operations and user input, your scripts transform from static calculators into dynamic, interactive tools that can communicate with users and handle varying data.

## Goals

Understand how to store and retrieve data using variables, manipulate text (strings), and make your programs interactive by accepting user input.

## Core Concepts

### Variables: Storing and Calling

Think of a variable as a labeled box where you can store a value. You use the equals sign (`=`) to assign a value to a variable name.  
Once stored, you can "call" (use) the variable by its name.

```python
# Storing values in variables
weight = 70
height = 1.75

# Calling the variables to perform a calculation
bmi = weight / height / height
print(bmi)

```

Variable names should be descriptive (e.g., `user_age` is better than `x`) and can contain letters, numbers, and underscores, but they cannot start with a number.

### String Operations

In Python, text is called a "String" and is enclosed in either single quotes (`'...'`) or double quotes (`"..."`).  
You can manipulate strings in several useful ways:

* Concatenation (Adding strings together):  
  Use the `+` operator to join strings.
  ```python
  greeting = "Hello, " + "World!"
  print(greeting) # Output: Hello, World!
  
  ```

* f-strings (Formatted strings):
  The most readable way to mix variables and text.  
  Just put an `f` before the opening quote and place your variables inside curly braces `{}`.
  ```python
  name = "Alice"
  age = 25
  print(f"My name is {name} and I am {age} years old.")
  
  ```

### User Input

To make your script interactive, use the `input()` function. It pauses the program and waits for the user to type something and press Enter.

```python
user_name = input("What is your name? ")
print(f"Nice to meet you, {user_name}!")

```

**Important Note:**  
The `input()` function *always* reads data as a string (text).  
If you want to do math with the user's input, you must convert it into a number using `int()` (for whole numbers) or `float()` (for decimals).

```python
age_text = input("Enter your age: ")
age_number = int(age_text) # Converts the text to an integer
print(f"Next year, you will be {age_number + 1}.")

```

## Guided Practice

* Step 1: Create a basic interactive script  
  Create a new file named `greeting.py`.  
  Use `input()` to ask the user for their name and store it in a variable called `name`.  
  Use an f-string to print a customized greeting.  
  Run the script using `python greeting.py` and test it.
* Step 2: Combine variables, input, and math  
  Create a new file named `dynamic_bmi.py`.  
  Ask the user for their weight in kg and height in meters using `input()`.  
  Remember to convert the inputs to floats:  
  `weight = float(input("Enter weight (kg): "))`.  
  Calculate the BMI and store it in a variable.
* Step 3: Format the output  
  Update your `dynamic_bmi.py` script to output a clean sentence using an f-string.  
  For example: `print(f"Your BMI is {bmi:.2f}")`.  
  (The `:.2f` inside the curly braces tells Python to show only 2 decimal places.)  
  Run the script and enter different numbers to see how the variables handle changing data.

## Checkpoints

* [ ] Write a currency converter script:  
      Ask the user to input an amount in USD.  
      Create a variable for the exchange rate (e.g., `exchange_rate = 31.5`).  
      Calculate the equivalent amount in TWD and print a sentence like:  
      `X USD is equal to Y TWD.`
* [ ] Use Python to solve the following problem:  
      Ask the user for their birth year.  
      Store the current year in a variable (e.g., `current_year = 2026`).  
      Calculate their age and print: "You are turning [Age] this year!"
