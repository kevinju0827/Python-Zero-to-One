# M09 Modules & File I/O

![Module 9 of 16](https://img.shields.io/badge/Module-9_of_16-6366f1?style=flat-square)
![Beginner](https://img.shields.io/badge/Difficulty-Beginner-4ade80?style=flat-square)
![1.5 hours](https://img.shields.io/badge/Time-1.5_hours-60a5fa?style=flat-square)
![Prerequisites: M01?08](https://img.shields.io/badge/Prerequisites-M01?08-94a3b8?style=flat-square)

**Topics covered:** `import` 繚 standard library (`os`, `datetime`, `math`, `random`) 繚 `pip` 繚 virtual environments (`venv`) 繚 `open()` 繚 reading and writing files

## The Why?

So far, every variable your scripts create disappears when the program exits.
A real application needs to **persist data** ??save a report to a file, read a configuration on startup, log activity to disk.

Python solves this in two complementary ways:

1. **Modules and packages** ??you do not write everything from scratch. Python's standard library includes hundreds of pre-built tools, and the broader ecosystem (PyPI) has hundreds of thousands more. Learning how to find, install, and manage these packages is what transforms you from a student writing scripts into a developer building applications.

2. **File I/O** ??reading and writing plain files. This is the simplest form of persistence, and it underpins CSV/JSON (M10), databases (M12), and almost every other data workflow in the course.

---

## Core Concepts

### `import` ??Using Modules

A module is a Python file that contains reusable code. You load it with `import`:

```python
import math
print(math.sqrt(16))   # 4.0
print(math.pi)         # 3.141592653589793
```

Or import specific names to avoid the prefix:

```python
from math import sqrt, pi
print(sqrt(25))   # 5.0
```

---

### The Standard Library ??Batteries Included

Python ships with hundreds of built-in modules. The ones you will use most often:

**`datetime` ??working with dates and times:**

```python
from datetime import datetime, timedelta

now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))   # e.g. 2026-05-27 14:30:00

tomorrow = now + timedelta(days=1)
print(tomorrow.date())
```

**`os` ??interacting with the operating system:**

```python
import os

print(os.getcwd())              # Current working directory
files = os.listdir(".")         # List all files in current folder
os.makedirs("output", exist_ok=True)  # Create a folder (no error if it exists)
```

**`random` ??generating random numbers:**

```python
import random

print(random.randint(1, 100))         # Random integer 1??00
print(random.choice(["a", "b", "c"])) # Random item from a list
random.shuffle(my_list)               # Shuffle a list in place
```

**`math` ??mathematical functions:**

```python
import math
math.floor(3.9)   # 3
math.ceil(3.1)    # 4
math.log(100, 10) # 2.0
```

---

### PyPI and `pip` ??Installing Third-Party Packages

The **Python Package Index (PyPI)** is a public repository of over 500,000 packages.
`pip` is the tool that downloads and installs them:

```bash
pip install requests        # Install the requests library
pip install requests==2.31  # Install a specific version
pip list                    # Show all installed packages
pip uninstall requests      # Remove a package
```

---

### Virtual Environments (`venv`) ??Project Isolation

Without a virtual environment, every package you install goes into the **global** Python installation. This causes conflicts when different projects need different versions of the same library.

A **virtual environment** is an isolated Python installation per project:

```bash
# Create a virtual environment inside your project folder
python -m venv .venv

# Activate it
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # macOS / Linux

# Install packages ??they go into .venv, not your global Python
pip install requests

# When done, deactivate
deactivate
```

**Best practice:** always create a virtual environment before installing packages for a project.

---

### File I/O ??Reading and Writing Files

Use `open()` to open a file. Always use the `with` statement ??it **automatically closes** the file even if an error occurs:

```python
# Writing a text file
with open("notes.txt", mode="w", encoding="utf-8") as f:
    f.write("First line\n")
    f.write("Second line\n")

# Reading the entire file
with open("notes.txt", mode="r", encoding="utf-8") as f:
    content = f.read()
    print(content)

# Reading line by line (memory-efficient for large files)
with open("notes.txt", mode="r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())   # .strip() removes the trailing newline
```

**File modes:**

| Mode | Meaning |
|------|---------|
| `"r"` | Read (default). Error if file does not exist. |
| `"w"` | Write. Creates file if missing; **overwrites** if it exists. |
| `"a"` | Append. Creates file if missing; adds to the end if it exists. |

Always specify `encoding="utf-8"` to avoid character encoding issues on Windows.

---

## Going Further

<details>
<summary>`pathlib` ??Modern File Paths</summary>

The `pathlib` module is the modern, object-oriented way to handle file paths (replaces `os.path`):

```python
from pathlib import Path

project = Path("my_project")
project.mkdir(exist_ok=True)

log_file = project / "log.txt"     # '/' joins path components
log_file.write_text("Hello!\n", encoding="utf-8")
print(log_file.read_text(encoding="utf-8"))
```

</details>

<details>
<summary>`requirements.txt` ??Sharing Dependencies</summary>

When collaborating, share the list of packages your project needs:

```bash
pip freeze > requirements.txt   # Save current packages to file
pip install -r requirements.txt  # Restore them on another machine
```

</details>

<details>
<summary>Reading a Binary File</summary>

Text mode (`"r"`, `"w"`) handles strings. Binary mode (`"rb"`, `"wb"`) handles raw bytes ??needed for images, PDFs, executables:

```python
with open("photo.jpg", mode="rb") as f:
    data = f.read()
    print(f"File size: {len(data):,} bytes")
```

</details>

<details>
<summary>Asking AI About Packages</summary>

When AI suggests a package you have never heard of:
1. Ask: *"What does [package] do and is it actively maintained?"*
2. Check PyPI for the last release date and download count.
3. Ask: *"Is there a standard library alternative that would work here?"*

</details>

---

## Guided Practice

We will build a **project deadline calculator** that reads a config file, computes time remaining, and writes a daily log entry.

### Step 1 ??Create and activate a virtual environment

Open a terminal inside the `M09Packages` folder:

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
```

### Step 2 ??Install `python-dateutil`

```bash
pip install python-dateutil
```

### Step 3 ??Write the deadline calculator

Create `deadline_calc_example.py`:

```python
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os

DEADLINE = "2026-12-31 23:59:59"
LOG_FILE = "deadline_log.txt"

deadline = datetime.strptime(DEADLINE, "%Y-%m-%d %H:%M:%S")
now      = datetime.now()
diff     = relativedelta(deadline, now)

report_lines = [
    "=== Project Deadline Tracker ===",
    f"Checked at  : {now.strftime('%Y-%m-%d %H:%M:%S')}",
    f"Target date : {DEADLINE}",
]

if deadline > now:
    remaining = f"{diff.months}m {diff.days}d {diff.hours}h remaining"
    report_lines.append(f"Status      : ON TRACK ??{remaining}")
else:
    report_lines.append("Status      : ??DEADLINE PASSED")

for line in report_lines:
    print(line)

# Append to a running log file
with open(LOG_FILE, mode="a", encoding="utf-8") as log:
    log.write("\n".join(report_lines) + "\n\n")

print(f"\nLog appended to {LOG_FILE}")
```

### Step 4 ??Inspect the log

Run the script twice. Open `deadline_log.txt` ??you should see two timestamped entries, not two overwrites. This is the difference between `"w"` and `"a"` modes.

---

## Checkpoints

* [ ] **Personal Activity Logger**
  Build a script that asks the user what they did today (one activity per line, empty line to finish).
  Append each activity to `activity_log.txt` with today's date as a header.
  On startup, if the log file exists, print the last 5 lines before asking for new input.
  *(Hint: `open(file, "a")` appends; `open(file, "r")` reads. Use `.readlines()[-5:]` to get the last 5 lines.)*

* [ ] **Batteries Included Challenge**
  Write a single script that uses four different standard library modules:
  1. `os` ??print the current working directory and list all `.py` files in it.
  2. `datetime` ??print the current date in `"Wednesday, 27 May 2026"` format.
  3. `random` ??pick a random motivational quote from a list of five you define.
  4. `math` ??calculate and print `??` and `?` to 10 decimal places.

* [ ] **Word Count Tool**
  Ask the user for a filename.
  Open the file (handle `FileNotFoundError` gracefully).
  Count total characters, total words (split by whitespace), and total lines.
  Print a formatted report. Write the report to a `_stats.txt` file next to the original.
