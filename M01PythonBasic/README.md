# M01 Python Basic

## The "Why?"

In real life, you'll often run into repetitive tasks – renaming hundreds of photos, downloading files from dozens of websites, crunching large datasets, or repeating the same reporting steps every day.

This is where programming shines: spending just ten minutes to write a small script can let your computer handle work that would otherwise take hours.

Once automated, the workflow becomes repeatable, scalable, and less error-prone.

Python is especially well-suited for these tasks because it’s straightforward to read and write, has a huge ecosystem of libraries, and works great for automation, data processing, and quick prototyping.

## Goals

Understand what python is and how to get started with Python and Vibe Coding (AI).

## Core Concepts

### Interactive mode

Unlike many programming languages (such as C, C#, Go, and Java), Python is an interpreted language.

In most cases, you don’t need a separate compiler toolchain to see results.

You simply write a script and call it to execute, and you'll immediately see the results.

This is most quickly demonstrated through Python's Interactive mode, which you can treat like a “calculator + mini lab” for experimenting with ideas, testing syntax, and doing quick computations.

### Line break and indentation

In Python, indentation is not just formatting — it is part of the syntax. 

Incorrect line breaks or indentation can cause errors, or worse: code that runs but behaves incorrectly.

If you’re coming from languages that use braces (`{}`) to define blocks, pay close attention: Python uses indentation to define blocks (for `if`, `for`, `while`, `def`, etc.).

Recommended habits:

- Use four spaces per indentation level (avoid mixing tabs and spaces)
- When debugging, check indentation consistency first
- Run small increments frequently to reduce debugging time

### Vibe coding

Vibe coding is a practical workflow for building software with AI as a collaborator.

You provide goals, constraints, context, and examples; the AI produces a draft solution; you run it, observe results, and iterate with feedback until it works reliably.

Python is a great match for Vibe Coding because it’s fast to run, straightforward to read, and gives immediate feedback.

AI can also call Python scripts directly. This extends the limitations of AI (complex calculations, operating systems).

> Reminder: AI is excellent at producing a first draft and exploring options, but it’s not a guarantee of correctness. Your job is not to trust it — it’s to verify it.

## Checkpoints

* [ ] Use Python interactive mode to calculate the following question:   
      Let's say you're 20 years old now and have 100,000 in savings.  
      If you invest this money in an index fund with an annualized return of 5% and reinvest the gains,  
      how much will you have when you retire at 60 (40 years from now)?  
      (Hint: `x ** y` can be used for power calculations.)
* [ ] Create a Python script file to solve the same problem above.
