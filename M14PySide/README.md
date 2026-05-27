# M14 GUI Development (PySide6)

![Module 14 of 16](https://img.shields.io/badge/Module-14_of_16-6366f1?style=flat-square)
![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-facc15?style=flat-square)
![~2 hours](https://img.shields.io/badge/Time-~2_hours-60a5fa?style=flat-square)
![Prerequisites: M01?13](https://img.shields.io/badge/Prerequisites-M01?13-94a3b8?style=flat-square)

**Topics covered:** PySide6 繚 `QApplication` 繚 widgets 繚 layouts 繚 signals & slots 繚 input validation 繚 `QMessageBox` 繚 combining GUI with SQLite and AI

## The Why?

Every script you have built so far runs in a terminal.
That is fine for you ??but hand any of those scripts to a friend, a manager, or your grandmother, and the first question will be: *"Why do I have to type commands? Where are the buttons?"*

A **Graphical User Interface (GUI)** ??windows, buttons, text boxes, menus ??is how non-programmers expect software to behave. **PySide6** is the official Python binding for **Qt**, the C++ framework behind professional applications like VLC, OBS Studio, Telegram Desktop, and Anaconda Navigator.

The transformation matters because it changes who can use your work. The expense tracker from M12, the AI rewriter from M16, the website monitor from M15 ??each of them stops being "a script" and starts being "a tool" the moment it has a window with buttons.

---

## Core Concepts

### Every PySide App Has the Same Shape

```python
import sys
from PySide6.QtWidgets import QApplication, QWidget

app    = QApplication(sys.argv)   # 1. Create the application object
window = QWidget()                 # 2. Create the window
window.setWindowTitle("My App")
window.show()                      # 3. Make it visible
sys.exit(app.exec())               # 4. Hand control to Qt's event loop
```

`app.exec()` starts the **event loop** ??Qt's infinite loop that listens for clicks, key presses, and OS messages. Your program "lives" inside this loop until the user closes the window.

---

### Widgets ??The Visual Building Blocks

A widget is any visible element. Common ones:

| Widget | Purpose | When to use |
|--------|---------|------------|
| `QLabel` | Read-only text or image | Titles, results, status |
| `QPushButton` | Clickable button | Triggering actions |
| `QLineEdit` | Single-line text input | Names, numbers, search |
| `QTextEdit` | Multi-line text input | Notes, long-form input |
| `QSpinBox` | Number input with ?聆 | Quantities, ratings |
| `QComboBox` | Drop-down list | Pick one from many |
| `QCheckBox` | Toggle checkbox | Yes/No options |

```python
from PySide6.QtWidgets import QLabel, QPushButton, QLineEdit

name_input  = QLineEdit()
name_input.setPlaceholderText("Enter your name??)

submit_btn  = QPushButton("Submit")
result_label = QLabel("Waiting for input??)
```

---

### Layouts ??Arranging Widgets Responsively

Never place widgets at absolute pixel coordinates ??the layout breaks on different screen sizes.
Use layout managers instead:

| Layout | Behavior |
|--------|----------|
| `QVBoxLayout` | Stack vertically (top ??bottom) |
| `QHBoxLayout` | Arrange horizontally (left ??right) |
| `QFormLayout` | Two columns: label on left, field on right |
| `QGridLayout` | 2D grid ??specify row and column |

```python
from PySide6.QtWidgets import QVBoxLayout

layout = QVBoxLayout()
layout.addWidget(result_label)
layout.addWidget(name_input)
layout.addWidget(submit_btn)
window.setLayout(layout)
```

Nest layouts freely: a `QHBoxLayout` of buttons can live inside a `QVBoxLayout` of panels.

---

### Signals and Slots ??How Widgets Talk to Your Code

A **signal** is something a widget emits when something happens (clicked, text changed, window closed).
A **slot** is a Python function connected to a signal.

```
widget.signal.connect(your_function)
```

```python
def on_submit():
    name = name_input.text()
    result_label.setText(f"Hello, {name}!")

submit_btn.clicked.connect(on_submit)
```

Common signals:
- `QPushButton.clicked`
- `QLineEdit.textChanged` ??fires on every keystroke
- `QLineEdit.returnPressed` ??fires when the user presses Enter
- `QComboBox.currentIndexChanged`

---

### Reading and Writing Widgets

| Action | Code |
|--------|------|
| Read text from input | `name_input.text()` |
| Write text to label | `result_label.setText("Hello!")` |
| Read number from spin box | `qty_spin.value()` |
| Read selected dropdown item | `combo.currentText()` |
| Disable a button | `btn.setEnabled(False)` |

---

### `QMessageBox` ??Pop-up Dialogs

```python
from PySide6.QtWidgets import QMessageBox

QMessageBox.information(window, "Saved", "Your file was saved successfully.")
QMessageBox.warning(window, "Error", "Please enter a valid number.")

reply = QMessageBox.question(window, "Confirm", "Delete this item?")
if reply == QMessageBox.StandardButton.Yes:
    delete_item()
```

---

## Going Further

<details>
<summary>`QTimer` ??Non-Blocking Timers</summary>

Never use `time.sleep()` in a GUI ??it freezes the entire interface.
Use `QTimer` instead:

```python
from PySide6.QtCore import QTimer

timer = QTimer()
timer.timeout.connect(update_display)
timer.start(1000)   # Call update_display() every 1000 ms
```

</details>

<details>
<summary>`QThread` ??Background Work Without Freezing</summary>

For long-running operations (API calls, file processing), run them in a `QThread` so the UI stays responsive. This is the right way to integrate Ollama (M16) calls into a GUI.

</details>

<details>
<summary>Stylesheets ??CSS for Qt Widgets</summary>

```python
window.setStyleSheet("""
    QPushButton {
        background-color: #6366f1;
        color: white;
        border-radius: 6px;
        padding: 8px;
    }
    QPushButton:hover { background-color: #4f46e5; }
""")
```

Qt's stylesheet syntax is similar to CSS.

</details>

<details>
<summary>Connecting GUI to SQLite (M12)</summary>

The two-step pattern for every database-backed button:

```python
def save_record():
    name = name_input.text()
    conn.execute("INSERT INTO contacts (name) VALUES (?)", (name,))
    conn.commit()
    refresh_list()   # Reload the display after saving
```

</details>

<details>
<summary>`QListWidget` ??Displaying a List</summary>

```python
from PySide6.QtWidgets import QListWidget

list_widget = QListWidget()
list_widget.addItem("Alice ??0912-111-222")
list_widget.addItem("Bob ??0923-333-444")
```

</details>

---

## Guided Practice

We will build a **tip calculator** ??a tiny desktop app a restaurant could actually use.

**Scenario:** A friend managing a small restaurant wants wait staff to be able to calculate tips quickly, without typing commands in a terminal.

### Step 1 ??Plan the layout

We need:
- `QLineEdit` for the bill amount
- `QSpinBox` for tip percentage (default 15%, range 0??0%)
- `QPushButton` to calculate
- `QLabel` to show results

### Step 2 ??Create the app skeleton

Create `tip_calculator_example.py`:

```python
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QFormLayout,
    QLineEdit, QSpinBox, QPushButton, QLabel, QMessageBox
)

app    = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Tip Calculator")
window.setFixedSize(320, 200)
```

### Step 3 ??Add widgets and layout

```python
bill_input  = QLineEdit()
bill_input.setPlaceholderText("e.g. 850.00")

tip_spin    = QSpinBox()
tip_spin.setRange(0, 30)
tip_spin.setValue(15)
tip_spin.setSuffix(" %")

calc_btn    = QPushButton("Calculate")
result_label = QLabel("Tip: ?nTotal: ??)

layout = QFormLayout()
layout.addRow("Bill Amount ($):", bill_input)
layout.addRow("Tip Percentage:", tip_spin)
layout.addRow(calc_btn)
layout.addRow(result_label)
window.setLayout(layout)
```

### Step 4 ??Wire the button

```python
def compute_tip():
    try:
        bill = float(bill_input.text())
    except ValueError:
        QMessageBox.warning(window, "Invalid Input", "Please enter a valid number for the bill amount.")
        return

    tip_pct = tip_spin.value() / 100
    tip     = bill * tip_pct
    total   = bill + tip
    result_label.setText(f"Tip:   ${tip:,.2f}\nTotal: ${total:,.2f}")

calc_btn.clicked.connect(compute_tip)
```

### Step 5 ??Launch and test the failure path

```python
window.show()
sys.exit(app.exec())
```

Run the script. Type `"abc"` in the bill field and click Calculate ??a clean warning dialog should appear instead of a crash. **This is the moment your script becomes real software.**

---

## Checkpoints

* [ ] **Pomodoro Timer (GUI Edition)**
  Re-implement the Pomodoro timer from M15 as a real desktop app:
  1. A large `QLabel` showing the time remaining (`"24:59"`).
  2. **Start**, **Pause**, and **Reset** buttons.
  3. A status label showing "Focus" or "Break".
  Use `QTimer` (not `time.sleep`) to update the display every second.
  *(Hint: search "PySide6 QTimer timeout" and connect its `timeout` signal to your tick function.)*

* [ ] **AI Email Polisher (Desktop App)**
  Wrap the polite-email rewriter from M16 in a GUI window:
  1. A `QTextEdit` for the rough draft.
  2. A "Polish" `QPushButton`.
  3. A second `QTextEdit` (read-only) for the polished output.
  4. A status `QLabel` showing "Idle" / "Polishing?? / "Done in X seconds".
  Disable the button while the model is running (re-enable after the response arrives).

* [ ] **Personal Bookmark Manager**
  Build a full CRUD desktop app combining M12 + M14:
  1. SQLite table `bookmarks(id, title, url, tag, added_on)`.
  2. A top form to add a new bookmark (title, URL, tag, Save button).
  3. A `QListWidget` displaying all bookmarks as `"[tag] title"`.
  4. A **Delete selected** button removing the highlighted entry from the list and the database.
  5. A search `QLineEdit` that filters the visible list in real time via `textChanged` + a SQL `LIKE` query.
