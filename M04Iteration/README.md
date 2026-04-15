# M04 Iteration

## The "Why?"

Humans generally dislike doing the exact same tedious task over and over again. Computers, on the other hand, excel at it.  
Imagine you need to rename 1,000 image files, send customized emails to 500 subscribers, or process thousands of rows in a dataset. Writing out the code for each individual item would take forever and defeat the purpose of programming.  
Iteration (commonly known as "loops") allows you to write a block of code once and have the computer repeat it as many times as needed.  
This is the core mechanic that unlocks the true scale and automation power of Python.

## Goals

Understand how to repeat actions using `for` and `while` loops, iterate over sequences of data, and control when a loop should stop.

## Core Concepts

### Lists

In Python, a "List" is a way to store multiple items in a single variable. You write a list using square brackets `[]`.

For example, a list can hold several fruits, movies, or any other values together in one place.

```python
fruits = ["apple", "banana", "cherry"]
```

### The `for` Loop and `range()`

A `for` loop is used when you know *exactly how many times* you want to repeat a task, or when you want to go through a specific sequence of items one by one.

A `for` loop makes it incredibly easy to process every item in a list.

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(f"I love eating {fruit}s!")
```

The `range()` function is often used with `for` loops to generate a sequence of numbers. By default, `range(5)` generates numbers from 0 up to (but not including) 5.

```python
# This will print 0, 1, 2, 3, 4
for i in range(5):
    print(f"Iteration number: {i}")
```

### The `while` Loop

A `while` loop is used when you want to repeat a task *until a certain condition changes*. It works similarly to an `if` statement, but instead of executing the code block just once, it keeps repeating it as long as the condition remains `True`.

Here is a flow chart illustrating how a `while` loop evaluates its condition before every single repetition:

```mermaid
graph TD
    Start([Start]) --> CheckCondition{"Condition is True?"}
    
    CheckCondition -- Yes --> ExecuteBlock["Execute loop body"]
    ExecuteBlock --> CheckCondition
    
    CheckCondition -- No --> Finish([End Loop / Continue Script])

```

> **Warning:** If the condition never becomes `False`, the loop will run forever! This is called an "infinite loop." Always make sure something inside the loop will eventually change the condition.

```python
countdown = 3

while countdown > 0:
    print(countdown)
    countdown = countdown - 1  # Decrease the value so the loop will eventually stop

print("Go!")

```

## Guided Practice

This guided practice asks you to build a program that calculates the pass rate for a midterm exam.  

* Step 1: Collect exam scores with a `while` loop  
  Create a file named `exam_stats.py`.  
  Create an empty list named `scores = []`.  
  Use a `while` loop to keep asking the user to enter exam scores.  
  If the input is a number, convert it to an integer and append it to `scores`.  
  If the input is not a number, stop collecting scores and continue to the next step.

* Step 2: Count passing and failing scores with a `for` loop  
  Create two variables: `pass_count = 0` and `fail_count = 0`.  
  Use a `for` loop to go through every score in `scores`.  
  Use `if else` to check whether each score is `>= 60` or `< 60`.  
  Increase `pass_count` for passing scores and `fail_count` for failing scores.

* Step 3: Print the statistics  
  Print the total number of scores entered, the number of passing scores, the number of failing scores, and the passing percentage.  
  Hint: the passing percentage can be calculated with:

  `pass_count / total_count * 100`

## Checkpoints

* [ ] Build a "Guess the Number" game:
  Use the `random` module to generate a secret number for the game.  
  For example, set `secret = random.randint(1, 100)` to choose a random number between 1 and 100.  
  Use a `while` loop to continuously ask the user to guess the number.  
  Add a helpful prompt so the user knows the valid range, such as "Guess a number between 1 and 100:".  
  Combine this with conditional logic (`if/elif/else`) from M03:
  - If the guess is too high, print "Too high, try again."
  - If the guess is too low, print "Too low, try again."
  - If they guess correctly, print "You got it!" and let the loop end.
