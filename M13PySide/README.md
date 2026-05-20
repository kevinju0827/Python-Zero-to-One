# M13 PySide (GUI Development)

## The "Why?"

Every script you have written so far runs in a terminal. That is fine for you—but if you handed any of those scripts to your friend, your manager, or your grandmother, the very first question would be: *"Why do I have to type commands? Where are the buttons?"*

A **Graphical User Interface (GUI)**—windows, buttons, text boxes, menus—is how non-programmers expect software to work. **PySide** is the official Python binding for **Qt**, the same C++ framework behind professional applications like VLC, OBS Studio, Maya, Telegram Desktop, and the Anaconda Navigator. Learning PySide lets you turn the data-processing logic from M08–M12 into something you can ship to people who have never opened a terminal in their life.

The transformation matters because it changes who can benefit from your work. The expense tracker from M10, the AI rewriter from M12, the website monitor from M11—each of them stops being a "Kevin's script" and starts being a "tool anyone can use" the moment it has a window with buttons.

## Goals

By the end of this module, you should be able to:

* Install PySide6 and run a "hello window" application.
* Explain the role of `QApplication`, `QWidget`, and the event loop (`app.exec()`).
* Use the most common widgets: `QLabel`, `QPushButton`, `QLineEdit`, `QTextEdit`, `QSpinBox`, `QComboBox`.
* Arrange widgets responsively using layouts (`QVBoxLayout`, `QHBoxLayout`, `QFormLayout`, `QGridLayout`).
* Connect a widget's **signal** (e.g., `clicked`) to a Python function (a **slot**).
* Read user input from widgets and write computed results back into the UI.
* Use `QMessageBox` to show warnings, confirmations, and informational dialogs.
* Combine PySide with previous modules (M10 SQLite, M12 Ollama) to turn data tools into desktop apps.

## Core Concepts

### Every PySide App Has the Same Shape

Every PySide program, from a one-button toy to Photoshop-sized monsters, starts and ends the same way:

```python
import sys
from PySide6.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)   # 1. Create the application object
window = QWidget()             # 2. Create a window
window.show()                  # 3. Tell it to appear on screen
sys.exit(app.exec())           # 4. Hand control to Qt's event loop
```

That last line is the most important one to understand. `app.exec()` does *not* exit immediately—it starts the **event loop**, an infinite loop run by Qt that listens for mouse clicks, key presses, and OS messages, and dispatches them to the right widgets. Your program "lives" inside this loop until the user closes the window.

This is the same idea as the `while True: schedule.run_pending()` loop from M11, but Qt manages the loop for you and does the dispatching of events to handler functions automatically.

---

### Widgets: The Visual Building Blocks

A **widget** is any visual element on the screen. The window itself is a widget; every button and label inside it is also a widget. The widgets you will use 90% of the time:

| Widget        | What it does                                | When to use it                  |
|---------------|---------------------------------------------|---------------------------------|
| `QLabel`      | Displays read-only text or an image         | Titles, results, status lines   |
| `QPushButton` | A clickable button                          | Triggering actions              |
| `QLineEdit`   | A single-line text input                    | Names, numbers, search queries  |
| `QTextEdit`   | A multi-line text input                     | Notes, long-form input          |
| `QSpinBox`    | A number input with up/down arrows          | Quantities, ages, ratings       |
| `QComboBox`   | A drop-down list                            | Picking one item from many      |
| `QCheckBox`   | A togglable checkbox                        | Yes/no options                  |

You instantiate them, set properties, and then add them to a layout:

```python
name_input = QLineEdit()
name_input.setPlaceholderText("Type your name...")

ok_button = QPushButton("Submit")
result_label = QLabel("Waiting for input...")
```

---

### Layouts: The Manager That Arranges Your Widgets

You *could* place widgets at absolute pixel positions, but that immediately breaks when the user resizes the window or runs your app on a different screen. The professional approach is to use a **layout manager** that handles arrangement for you.

| Layout         | Behavior                                                        |
|----------------|-----------------------------------------------------------------|
| `QVBoxLayout`  | Stack widgets **vertically**, top to bottom                     |
| `QHBoxLayout`  | Arrange widgets **horizontally**, left to right                 |
| `QFormLayout`  | Two columns: a **label** on the left, a **field** on the right  |
| `QGridLayout`  | A 2D grid—specify row and column for each widget                |

You can also nest layouts: a `QVBoxLayout` can contain a `QHBoxLayout`, which contains buttons side by side, while the outer layout keeps a label above and a result panel below. This is how every real Qt app is constructed.

```python
layout = QVBoxLayout()
layout.addWidget(QLabel("Name:"))
layout.addWidget(name_input)
layout.addWidget(ok_button)
layout.addWidget(result_label)
window.setLayout(layout)
```

---

### Signals and Slots: How Widgets Talk to Your Code

A **signal** is something a widget "emits" when something happens to it (the button was clicked, the text changed, the window was resized). A **slot** is just a Python function that you connect to a signal. When the signal fires, the slot runs.

```python
def on_submit():
    name = name_input.text()
    result_label.setText(f"Hello, {name}!")

ok_button.clicked.connect(on_submit)
```

The pattern is always the same: `widget.signalName.connect(your_function)`. Common signals worth knowing:

* `QPushButton.clicked` — the button was clicked.
* `QLineEdit.textChanged` — the text in the box changed (fires on every keystroke).
* `QLineEdit.returnPressed` — the user pressed Enter inside the box.
* `QComboBox.currentIndexChanged` — a different item was selected.

---

### Dialogs: Pop-up Messages

For confirmations, warnings, and quick info messages, use `QMessageBox`:

```python
from PySide6.QtWidgets import QMessageBox

QMessageBox.information(window, "Saved", "Your file was saved successfully.")
QMessageBox.warning(window, "Oops", "Please enter a valid number.")

# A yes/no confirmation:
reply = QMessageBox.question(window, "Confirm", "Delete this contact?")
if reply == QMessageBox.Yes:
    delete_contact()
```

This is the standard way to communicate with the user outside of the main window.

---

### Reading from and Writing to Widgets

The vocabulary you will use most often:

| Action                   | Code                          |
|--------------------------|-------------------------------|
| Read text from a field   | `name_input.text()`           |
| Write text to a label    | `result_label.setText("...")` |
| Read number from spinbox | `qty_input.value()`           |
| Read selected dropdown   | `combo.currentText()`         |
| Disable a button         | `submit_button.setEnabled(False)` |

The two-step "read inputs → compute → write to output widget" loop is the heart of almost every GUI handler function you will write.

---

## Guided Practice

We will build a **tip calculator**—a tiny window the staff at a restaurant could actually use, exercising every PySide concept above: widgets, a `QFormLayout`, signal-to-slot wiring, input validation, and `QMessageBox` for warnings.

**Scenario**: A friend who manages a small restaurant wants a tool the wait staff can run when paying out at the end of the night. A terminal script with `input()` would intimidate them; a window with two fields and a button will not.

**Step 1: Plan the widgets.** Three inputs and one output:
* `QLineEdit` for the bill amount (a free-text field so the user can type cents).
* `QSpinBox` for the tip percentage, with a sensible default (15) and range (0–30).
* `QPushButton` to trigger the calculation.
* `QLabel` to display `"Tip: $X.XX"` and `"Total: $Y.YY"`.

**Step 2: Arrange them in a `QFormLayout`.** This gives a clean two-column "label : field" layout for free. Set the window title and size so the app feels intentional, not a debugger leak.

**Step 3: Wire the button's `clicked` signal to a `compute_tip()` slot.** Inside the slot:
1. Read the bill text. Convert to `float` inside a `try/except ValueError`.
2. On failure, show `QMessageBox.warning(window, "Invalid input", ...)` and return. **Never let bad input crash the app**—a polished GUI handles invalid data gracefully.
3. On success, multiply by the spin-box value, format with `f"{value:,.2f}"`, and write the result to the output label.

**Step 4: Try the failure path.** Type `"abc"` into the bill field and click Calculate. A clean warning dialog should appear instead of a traceback. This is the moment your script becomes "real software."

The full implementation is in `tip_calculator_example.py`. Read every line—it is short, and it shows the canonical shape of every PySide app you will write from now on (`QApplication` → window → widgets → layout → `app.exec()`).

---

## Checkpoints

* [ ] **The Pomodoro Timer (GUI Edition)**:
      Re-implement the Pomodoro timer from M11 as a real desktop app. It should have:
      1. A large `QLabel` showing the time remaining (`"24:59"`).
      2. Buttons to **Start**, **Pause**, and **Reset**.
      3. A status line that says whether the user is currently in "Focus" or "Break".
      Use Qt's `QTimer` (not `time.sleep`!) to update the label every second—blocking with `time.sleep` would freeze the entire UI.
      *(Hint: search for "PySide6 QTimer timeout" and connect its `timeout` signal to your "tick" function. Learning when to use a non-blocking timer instead of `sleep` is exactly the kind of pivot that GUI development forces on you.)*

* [ ] **AI Email Polisher (Desktop App)**:
      Wrap the polite-email-rewriter from M12 in a GUI. The window should have:
      1. A `QTextEdit` for the **rough draft**.
      2. A `QPushButton` labeled "Polish".
      3. A second `QTextEdit` (read-only) for the **polished output**.
      4. A status `QLabel` at the bottom showing "Idle" / "Polishing..." / "Done in 4.2 seconds".
      While the model is generating, the Polish button should be **disabled** so the user cannot click it twice. Re-enable it after the response comes back.
      *(Hint: Ollama calls can take several seconds. A polished version of this would use `QThread` to keep the UI responsive, but for a first pass it is fine if the window briefly freezes. Be honest about this limitation when you describe your work.)*

* [ ] **Personal Bookmark Manager**:
      Build a small CRUD app entirely from scratch that combines what you have learned in M10, M13 (this module), and a bit of layout sense:
      1. A SQLite table `bookmarks(id, title, url, tag, added_on)`.
      2. A top form to add a new bookmark (`title`, `url`, `tag`, and a Save button).
      3. A `QListWidget` showing all bookmarks (display them as `"[tag] title — url"`).
      4. A **Delete selected** button that removes the highlighted entry from both the list and the database.
      5. A search `QLineEdit` whose `textChanged` signal filters the visible list by `title` or `tag` in real time.
      *(Hint: connect `searchBox.textChanged.connect(refresh_list)` and inside `refresh_list` run a SQL query with `WHERE title LIKE ? OR tag LIKE ?`. Live-as-you-type filtering is one of those small touches that turns a "school project" into a tool you would actually use.)*
