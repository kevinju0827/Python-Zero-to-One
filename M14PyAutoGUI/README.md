# M14 PyAutoGUI (Desktop Automation)

## The "Why?"

In M09 you talked to systems through clean web APIs. In M10 you talked to a database through SQL. In both cases, the software was *designed* to be talked to. But the real world is full of software that wasn't: a legacy accounting program from 2003, an internal portal with no API, a stubborn website that rejects every kind of scripted access, a desktop tool whose vendor went out of business. When there is no API to call and no database to query, you have one option left: **drive the application the same way a human would**—move the mouse, click buttons, type text, take screenshots.

**PyAutoGUI** is the Python library that turns your script into a virtual user. It can move the cursor to a pixel coordinate, click, press keys, type strings, take screenshots, and even *find* an image on the screen and click on it. It is the same category of tool that office automation teams use to migrate data between systems that vendors refuse to integrate, and it is the practical "duct tape" that holds together many real-world business processes.

A serious word of warning before we begin: PyAutoGUI literally controls your machine. A loop that clicks in the wrong place can do real damage—close unsaved work, send a half-typed message, click "delete" on the wrong file. Learning to use it responsibly is just as important as learning the API itself.

## Goals

By the end of this module, you should be able to:

* Install PyAutoGUI and confirm it can read your mouse position.
* Use the screen coordinate system (top-left origin, X increases right, Y increases down).
* Enable the fail-safe and a global `PAUSE` so a runaway script can be stopped safely.
* Move the mouse, click, and double-click using `moveTo`, `click`, and `doubleClick`.
* Type text and press keys using `write`, `press`, and `hotkey`.
* Take screenshots with `screenshot` and save them with `os` + `datetime` for organization.
* Find a target element on the screen using `locateOnScreen` with an image template.
* Recognize when PyAutoGUI is the *right* tool and when an API would be safer and faster.

## Core Concepts

### Screen Coordinates

PyAutoGUI thinks of the screen as a grid:

* `(0, 0)` is the **top-left** corner.
* `X` increases as you move right.
* `Y` increases as you move *down* (this is the opposite of math class).

You can ask for the current cursor position any time:

```python
import pyautogui
x, y = pyautogui.position()
print(x, y)
```

The total screen size is also available:

```python
width, height = pyautogui.size()
```

If your machine uses multiple monitors or display scaling, the coordinates can shift unexpectedly. This is normal and is one of the reasons automation scripts can be brittle.

---

### The Fail-Safe Is Not Optional

If your script enters a runaway loop and starts clicking things it shouldn't, you need a guaranteed way to stop it. PyAutoGUI's fail-safe is exactly that: when your cursor reaches *any one of the four screen corners*, the next PyAutoGUI call raises a `FailSafeException` and the script halts.

Always enable it at the top of every script you write in this module:

```python
import pyautogui

pyautogui.FAILSAFE = True   # Slam the mouse into a corner to abort
pyautogui.PAUSE = 0.5       # Wait half a second between every action
```

The `PAUSE` setting forces a small delay between every PyAutoGUI command. It both gives the host application time to respond and gives *you* a window to fling the cursor into a corner if something looks wrong.

---

### Mouse Actions

```python
pyautogui.moveTo(500, 300, duration=0.5)   # Smoothly move over half a second
pyautogui.click()                          # Click the left button at current position
pyautogui.click(x=200, y=400)              # Move and click in one call
pyautogui.doubleClick()
pyautogui.rightClick()
pyautogui.scroll(-3)                       # Scroll down 3 "clicks"
```

The `duration` argument is more than cosmetic—a slow movement is easier to follow visually when you are debugging and easier on apps that rely on hover effects.

---

### Keyboard Actions

```python
pyautogui.write("Hello, world!", interval=0.05)   # Type a string
pyautogui.press("enter")                          # Press a single key
pyautogui.press("tab")
pyautogui.hotkey("ctrl", "c")                     # Press Ctrl+C (copy)
pyautogui.hotkey("alt", "tab")                    # Press Alt+Tab
```

Note that `write()` can only produce characters that appear on a US keyboard. For special characters or non-Latin scripts (Chinese, Japanese, accented letters), you typically have to copy the text into the clipboard first and then paste it with `pyautogui.hotkey("ctrl", "v")`.

---

### Screenshots

`pyautogui.screenshot()` returns an in-memory image of the entire screen. You can pass a filename to save it directly:

```python
pyautogui.screenshot("desktop.png")                   # Whole screen
pyautogui.screenshot("region.png", region=(0, 0, 800, 600))  # Top-left rectangle
```

Combine this with `datetime.now()` to keep a folder of timestamped screenshots that never overwrite each other—useful for audit trails or for debugging an automation that runs while you are away from the desk.

---

### Finding Elements by Image

The clicked coordinate of a button can change if the window moves. A more robust approach is **image matching**: save a small PNG of the button you want to click, then ask PyAutoGUI to find it on the screen:

```python
location = pyautogui.locateOnScreen("save_button.png", confidence=0.8)
if location is not None:
    pyautogui.click(pyautogui.center(location))
```

The `confidence` parameter (requires `pip install opencv-python`) makes the match tolerant to anti-aliasing differences. This technique trades brittleness with coordinates for brittleness with visual themes (the image won't match if the user changes their color scheme), but it is generally more robust than hard-coded XY positions.

---

### Defensive Automation: Slow, Sleepy, Skeptical

A few rules every automation script you write should follow:

1. **Open the script with `FAILSAFE = True` and a `PAUSE` of at least 0.2 seconds.** Never disable the fail-safe.
2. **Give the user a countdown** (`for i in range(5, 0, -1): print(...); time.sleep(1)`) before any clicking starts, so they have time to switch to the right window.
3. **Verify before destructive actions.** If your script is about to click "Delete," consider taking a `screenshot()` first as evidence.
4. **Never run an automation on a machine that has unsaved work open.** Treat scripted control like power tools—respect the blast radius.

---

## Guided Practice

We will build a **scheduled screenshot logger**—a small automation that quietly captures the screen every few seconds and saves each frame with a sortable timestamp. It exercises every safety habit from above (`FAILSAFE`, defensive `try/except`) and combines PyAutoGUI with the `schedule` library from M11.

**Scenario**: You're debugging a flaky issue that only happens "sometimes during the day"—nobody can reproduce it on demand. A quiet logger that takes a screenshot every few minutes gives you visual evidence of what was on screen when the next report comes in. The same pattern shows up in remote-work tools and security audit trails.

**Step 1: Set the safety flags first.** At the top of the script, set `pyautogui.FAILSAFE = True`. Even though this script doesn't move the mouse, the habit of enabling fail-safe on every PyAutoGUI script will save you when you later add clicks.

**Step 2: Prepare the output folder.** Use `os.makedirs("screenshots", exist_ok=True)` so the folder is created on first run but not re-created on subsequent runs.

**Step 3: Write `capture_now()`.** Generate a sortable filename like `2026-05-20_14-30-15.png` with `datetime.now().strftime(...)`. Call `pyautogui.screenshot(path)`. Wrap the call in `try/except`—a transient screen-access issue should *log* the problem and let the scheduler continue, not crash the whole program.

**Step 4: Schedule and loop.** Call `capture_now()` once at startup so the user sees immediate feedback that the script is alive. Then `schedule.every(10).seconds.do(capture_now)` (10 seconds is fine for testing; bump to minutes for real use). The main loop is `schedule.run_pending()` + `time.sleep(1)` inside `try/except KeyboardInterrupt`.

**Step 5: Verify.** Let it run for ~30 seconds, press Ctrl+C, then open the `screenshots/` folder. The filenames sort chronologically because they start with the date.

The full implementation is in `screenshot_logger_example.py`. This is your first cross-module automation—PyAutoGUI for capture, `schedule` for timing, the filesystem for persistence—in one short script.

---

## Checkpoints

* [ ] **Anti-AFK Mouse Mover**:
      Some apps (chat tools, time trackers, remote-desktop sessions) mark you as "away" after a few minutes of inactivity. Build a script that, every 60 seconds, nudges the mouse by a few pixels and returns it—just enough movement to register as activity, but small enough that it does not interfere with what you are actually doing.
      Requirements:
      1. Record the current mouse position, move it by `(+3, 0)` over half a second, then move back to where it was.
      2. Run the cycle indefinitely until the user presses Ctrl+C.
      3. Print a one-line status message each cycle: `"[12:01:00] nudged"`.
      *(Hint: be honest about whether your IT policy permits this kind of script. The point of this checkpoint is to demonstrate that you understand subtle automation patterns and their ethical implications—not to encourage you to actually deploy one against your employer.)*

* [ ] **Form Auto-Filler from a CSV**:
      Your friend running a tutoring business (recall M12 Practice 2) has 30 student registration emails she has now manually extracted into a `students.csv` file with columns `name`, `grade`, `subject`, `phone`. The school's online system has no API—each row must be typed into a web form by hand. Build a script that:
      1. Opens a text editor (manually) before the script starts.
      2. Reads `students.csv` (recall M08).
      3. For each row, types `"{name} | grade {grade} | {subject} | {phone}"` and presses Enter.
      4. Pauses 1 second between rows—real systems often need this to keep up.
      *(Hint: even though we are typing into Notepad here, the exact same pattern works for filling out web forms—you `Tab` between fields and `write()` each value. Build this for Notepad first, then imagine how you would modify it for a real form on an unfamiliar site.)*

* [ ] **Personal Time-Lapse Builder**:
      Combine M11, M14, and M16 (the next module) for one of the most fun side projects you can build:
      1. Every 30 seconds for the duration of a work session (use `schedule`), take a screenshot and save it into a `frames/` folder.
      2. When the user presses Ctrl+C, your script should print how many frames were captured.
      3. *(Optional stretch—revisit after M16)* Use OpenCV to stitch all the frames into an MP4 timelapse video of your day at the computer.
      Requirements for now: focus on the *capture loop* and the *organized filenames*. Decide on a sensible filename scheme (`frame_000001.png`, `frame_000002.png`) so they sort correctly in alphabetical order—this matters when M16 reads them back in.
      *(Hint: this is the same pattern Twitch streamers and YouTubers use to record "coding day in my life" content—you are about to build the engine.)*
