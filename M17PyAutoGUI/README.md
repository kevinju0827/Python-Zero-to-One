# M17 Desktop Automation (PyAutoGUI)

![Module 17 of 17](https://img.shields.io/badge/Module-17_of_17-6366f1?style=flat-square)
![Intermediate](https://img.shields.io/badge/Difficulty-Intermediate-facc15?style=flat-square)
![1.5 hours](https://img.shields.io/badge/Time-1.5_hours-60a5fa?style=flat-square)
![Prerequisites: M01–M16](https://img.shields.io/badge/Prerequisites-M01–M16-94a3b8?style=flat-square)

**Topics covered:** screen coordinates · fail-safe · `PAUSE` · mouse actions · keyboard actions · screenshots · `locateOnScreen` · defensive automation practices

## The Why?

In M11 you talked to systems through clean web APIs. In M12 you talked to a database through SQL. In both cases, the software was *designed* to be programmed.

But the real world is full of software that was not: a legacy accounting application from 2003, an internal HR portal with no API, a desktop tool whose vendor went bankrupt. When there is no API and no database to query, you have one option: **drive the application exactly as a human would** — move the mouse, click buttons, type text, take screenshots.

**PyAutoGUI** turns your script into a virtual user. It is the same category of tool that office automation teams use to migrate data between systems that refuse to integrate — and the practical "duct tape" that holds together many real business processes.

> **⚠ Safety warning:** PyAutoGUI literally controls your machine. A loop that clicks in the wrong place can close unsaved work, send a half-typed message, or click "delete" on the wrong file. Learning to use it **responsibly** is as important as learning the API itself. Always test on a clean screen with nothing important open.

---

## Core Concepts

### Screen Coordinates

PyAutoGUI uses a pixel grid:
- `(0, 0)` is the **top-left** corner of your primary monitor.
- `X` increases going right.
- `Y` increases going **down** (opposite of math class).

```python
import pyautogui

x, y = pyautogui.position()           # Current cursor position
width, height = pyautogui.size()       # Screen resolution
print(f"Cursor at ({x}, {y}) on a {width}×{height} screen")
```

Multiple monitors and display scaling can shift coordinates unpredictably — one reason automation scripts can be brittle.

---

### The Fail-Safe — Non-Negotiable

Moving the cursor to any screen corner raises a `FailSafeException` and halts your script.
**Enable it at the top of every script you write in this module:**

```python
import pyautogui

pyautogui.FAILSAFE = True   # Move cursor to a corner to abort instantly
pyautogui.PAUSE   = 0.5     # Half-second pause between every action
```

`PAUSE` gives the host application time to respond — and gives *you* a window to fling the cursor to a corner if something goes wrong.

---

### Mouse Actions

```python
pyautogui.moveTo(500, 300, duration=0.5)   # Smooth move over 0.5 seconds
pyautogui.click()                          # Left-click at current position
pyautogui.click(x=200, y=400)             # Move and click in one call
pyautogui.doubleClick()
pyautogui.rightClick()
pyautogui.scroll(-3)                       # Scroll down 3 "notches"
```

---

### Keyboard Actions

```python
pyautogui.write("Hello!", interval=0.05)  # Type a string, 50ms between chars
pyautogui.press("enter")
pyautogui.press("tab")
pyautogui.hotkey("ctrl", "c")             # Ctrl+C (copy)
pyautogui.hotkey("ctrl", "v")             # Ctrl+V (paste)
pyautogui.hotkey("alt", "tab")            # Switch windows
```

> **Note:** `write()` types characters as if pressing keys. For non-ASCII text (Chinese, accented letters), copy the text to the clipboard first and paste with `hotkey("ctrl", "v")`.

---

### Screenshots

```python
pyautogui.screenshot("desktop.png")                        # Whole screen
pyautogui.screenshot("region.png", region=(0, 0, 800, 600)) # Top-left 800×600
```

Combine with `datetime` to generate timestamped filenames that never overwrite each other — useful for audit trails and debugging runs that happen while you are away.

---

### Finding Elements by Image

Instead of hard-coding pixel coordinates (which break if the window moves), save a small PNG of the button you want to click and let PyAutoGUI find it:

```python
location = pyautogui.locateOnScreen("save_button.png", confidence=0.8)
if location:
    pyautogui.click(pyautogui.center(location))
else:
    print("Button not found on screen.")
```

`confidence` (requires `pip install opencv-python`) makes matching tolerant to minor anti-aliasing differences.

---

### Defensive Automation — Four Rules

1. **Always enable `FAILSAFE = True` and set `PAUSE ≥ 0.2`.**
2. **Give the user a countdown** before clicking starts, so they can switch to the right window.
3. **Take a screenshot** before any destructive action as evidence of what was on screen.
4. **Never run on a machine with unsaved work open.** Treat scripted control like power tools.

---

## Going Further

<details>
<summary>Clipboard Manipulation</summary>

For pasting non-ASCII characters or large blocks of text:

```python
import pyperclip   # pip install pyperclip

pyperclip.copy("你好世界")
pyautogui.hotkey("ctrl", "v")
```

</details>

<details>
<summary>Matching with Different Confidence Levels</summary>

A lower confidence value (`0.6`) catches the button even when the theme changes; too low and you get false positives:

```python
# Start at 0.9, lower if it fails to find things
location = pyautogui.locateOnScreen("button.png", confidence=0.85)
```

</details>

<details>
<summary>Multi-Monitor Coordinates</summary>

On Windows with multiple monitors, the primary monitor starts at `(0, 0)`. Secondary monitors extend into negative or larger positive X values depending on their arrangement. Test `pyautogui.position()` while moving the cursor to each monitor to learn your layout.

</details>

<details>
<summary>Ethical and Policy Considerations</summary>

Before deploying an automation script at work:
- Check your company's acceptable-use policy.
- Never use automation to forge input, bypass audit trails, or misrepresent activity.
- The anti-AFK checkpoint below is explicitly included to prompt this reflection — not to encourage policy violations.

</details>

---

## Guided Practice

We will build a **scheduled screenshot logger** — a script that quietly captures the screen at intervals and saves each frame with a sortable timestamp. The same pattern powers remote-work tools and security audit trails.

**Scenario:** You are debugging a flaky issue that only appears "sometimes during the day." A background logger that takes screenshots every few minutes gives you visual evidence of what was on screen when it happened next.

### Step 1 — Set safety flags and prepare the folder

Create `screenshot_logger_example.py`:

```python
import pyautogui
import schedule
import time
import os
from datetime import datetime

pyautogui.FAILSAFE = True

os.makedirs("screenshots", exist_ok=True)
```

### Step 2 — Write the capture function

```python
def capture_now():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path      = os.path.join("screenshots", f"{timestamp}.png")
    try:
        pyautogui.screenshot(path)
        print(f"[{timestamp}] Captured → {path}")
    except Exception as e:
        print(f"[{timestamp}] Capture failed: {e}")
```

Wrapping in `try/except` means a transient screen-access issue logs a warning instead of crashing the scheduler.

### Step 3 — Schedule and run

```python
capture_now()   # Run once immediately so you see feedback right away

schedule.every(10).seconds.do(capture_now)   # Every 10s for testing

print("\nLogger running. Press Ctrl+C to stop.\n")
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nLogger stopped.")
```

### Step 4 — Verify

Let it run for ~30 seconds, press Ctrl+C, then open the `screenshots/` folder.
The filenames sort chronologically because they start with the date and time.
This naming scheme matters — when you have 500 frames, alphabetical sort must equal chronological sort.

---

## Checkpoints

* [ ] **Anti-AFK Mouse Nudger**
  Some apps (chat tools, remote desktop) mark you "away" after inactivity.
  Build a script that, every 60 seconds:
  1. Records the current mouse position.
  2. Moves it by +3 pixels to the right (half a second duration).
  3. Moves it back to the original position.
  4. Prints a status line: `"[HH:MM:SS] nudged"`.
  Loop until Ctrl+C.
  *(Important: reflect on whether your IT policy permits this before ever deploying it. The goal of this checkpoint is to understand subtle automation patterns and their ethical implications.)*

* [ ] **CSV Form Auto-Filler**
  A colleague has a `students.csv` with columns `name`, `grade`, `subject`, `phone`.
  Build a script that opens Notepad (or TextEdit on Mac) before running, then:
  1. Reads the CSV (recall M10).
  2. For each row, types `"{name} | grade {grade} | {subject} | {phone}"` and presses Enter.
  3. Waits 0.5 seconds between rows.
  *(Hint: give a 5-second countdown at the start so you can click into Notepad before the typing begins. The same pattern works for real web forms — you Tab between fields and write() each value.)*

* [ ] **Personal Time-Lapse Builder**
  Capture screenshots every 30 seconds into a `frames/` folder during a work session.
  Name frames `frame_000001.png`, `frame_000002.png`, etc. so they sort correctly alphabetically.
  When the user presses Ctrl+C, print how many frames were captured and the total session duration.
