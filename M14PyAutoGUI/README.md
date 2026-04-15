# M14 PyAutoGUI (Desktop Automation)

## The "Why?"

Sometimes, the software you want to automate doesn't have an API or a database you can connect to. Maybe it's an old accounting software, a complex desktop application, or a website that blocks automated bots. In these cases, you can use **PyAutoGUI** to control the mouse and keyboard just like a human would. You can tell Python to "move to this button," "click," and "type this text." It's like having a robot sitting at your desk, performing boring, repetitive tasks for you.

## Goals

Learn how to control the mouse cursor, simulate keyboard keypresses, and use basic safety features to prevent your automation scripts from going out of control.

## Core Concepts

### Screen Coordinates
Your screen is a grid of pixels. The top-left corner is `(0, 0)`. PyAutoGUI uses these X and Y coordinates to know exactly where to move the mouse or where to click.

### Fail-Safe (Safety First!)
**Crucial!** If your script starts clicking things it shouldn't, move your mouse cursor to any of the four corners of your screen. This will trigger a `FailSafeException` and stop the script immediately.

### Primary Actions
- `pyautogui.moveTo(x, y)`: Moves the mouse to a specific location.
- `pyautogui.click()`: Clicks the left mouse button.
- `pyautogui.write("text")`: Types a string of text.
- `pyautogui.press("enter")`: Presses a specific key on the keyboard.

## Guided Practice

We will write a "Ghost Writer" script that opens the Windows Notepad app (or any text editor) and types a message automatically.

*   **Step 1: Install PyAutoGUI**
    ```bash
    pip install pyautogui
    ```

*   **Step 2: Create `ghost_writer_example.py`**
    ```python
    import pyautogui
    import time

    # Give yourself 3 seconds to switch to your text editor!
    print("Automation starting in 3 seconds... Switch to Notepad or a text editor!")
    time.sleep(3)

    # 1. Type a message slowly (interval makes it look like a human is typing)
    message = "Hello! This message was typed automatically by a Python script."
    pyautogui.write(message, interval=0.1) 

    # 2. Press Enter to go to a new line
    pyautogui.press('enter')

    # 3. Type another line
    pyautogui.write("Desktop automation with PyAutoGUI is amazing!", interval=0.1)

    print("Task Complete.")
    ```

## Checkpoints

* [ ] **Coordinate Finder**:
    Write a script that prints the current mouse position (`pyautogui.position()`) every second in a loop. Use this to find the coordinates of your browser's "Refresh" button.
* [ ] **Automated App Launcher**:
    Write a script that: 1. Presses the "Win" key. 2. Types "Calculator". 3. Presses "Enter". 4. Waits 2 seconds. 5. Types "123+456=".
* [ ] **The Screen Grabber**:
    Use `pyautogui.screenshot()` to take a picture of your desktop and save it as `my_desktop.png`. Research how to add a timestamp (from M07) to the filename so you don't overwrite old screenshots.