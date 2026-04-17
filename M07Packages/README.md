# M07 Packages

## The "Why?"

In modern software development, you rarely write every single piece of functionality from scratch. Python’s greatest strength is its massive ecosystem of pre-written code called **packages**. Whether you need to perform complex data analysis, connect to a database, or even control a robot, there is likely a package already built for it. Learning how to find, install, and manage these packages is what transforms you from a student writing scripts into a developer building applications.

## Goals

Understand how to use Python's built-in **Standard Library**, how to install third-party packages using **pip**, and how to use **Virtual Environments** to keep your project dependencies organized and isolated.

## Core Concepts

### The Standard Library
Python comes with "batteries included." This means it has a vast collection of built-in modules for common tasks like mathematical operations (`math`), generating random numbers (`random`), or handling dates and times (`datetime`).
```python
import datetime
print(f"Current time: {datetime.datetime.now()}")
```

### PyPI and `pip`
The **Python Package Index (PyPI)** is a public repository of software for the Python programming language. `pip` is the standard package manager for Python, used to install and manage additional libraries that are not part of the standard library.
```bash
pip install requests
```

### Virtual Environments (`venv`)
A virtual environment is an isolated environment that allows you to install packages without affecting other projects or the global Python installation. This is a "Best Practice" in Python development.
- **Create**: `python -m venv .venv`
- **Activate (Windows)**: `.venv\Scripts\activate`
- **Activate (macOS/Linux)**: `source .venv/bin/activate`

## Guided Practice

In a real-world project, you often need to handle dates beyond simple formatting—like calculating how many business days are left until a deadline. We will use the `python-dateutil` package for this.

*   **Step 1: Create and Activate a Virtual Environment**
    Open your terminal in the `M07Packages` folder:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate  # Windows
    # source .venv/bin/activate  # macOS/Linux
    ```

*   **Step 2: Install the Package**
    ```bash
    pip install python-dateutil
    ```

*   **Step 3: Create `deadline_calc_example.py`**
    We will use the `relativedelta` from `dateutil` to find the exact difference between now and a project deadline.
    ```python
    from datetime import datetime
    from dateutil.relativedelta import relativedelta

    deadline_str = "2026-12-31 23:59:59"
    deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")

    now = datetime.now()

    diff = relativedelta(deadline, now)

    print("--- Project Deadline Tracker ---")
    print(f"Target Date: {deadline_str}")
    print(f"Current Date: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 32)

    if deadline > now:
        print(f"Time remaining: {diff.years} years, {diff.months} months, {diff.days} days, {diff.hours} hours.")
    else:
        print("The deadline has already passed!")
    ```

## Checkpoints

* [ ] **The "Batteries Included" Challenge**:
    Use the standard `os` module to list all files in your current directory. Then use the `platform` module to print your computer's operating system name.
