# M13 PySide (GUI Development)

## The "Why?"

Most people don't use a terminal to interact with software; they use buttons, menus, and windows. To build applications that your friends, family, or colleagues can easily use, you need a **Graphical User Interface (GUI)**. **PySide** (the official Python module for Qt) is one of the most powerful and professional toolkits for building desktop apps. It allows you to create everything from simple tools to complex software like Photoshop, Maya, or the VLC Media Player.

## Goals

Learn the basics of window creation, how to arrange "widgets" (buttons, text boxes, labels) using layouts, and how to make those widgets respond to user actions like clicking.

## Core Concepts

### Widgets
Widgets are the visual building blocks of a GUI:
- `QLabel`: Displays text or images.
- `QPushButton`: A button you can click.
- `QLineEdit`: A single-line box where the user can type text.

### Layouts
Instead of placing buttons at exact pixel coordinates (which break when you resize the window), we use **Layouts** (like `QVBoxLayout` for vertical stacking) to automatically manage the position and size of our widgets.

### Signals and Slots
This is how PySide handles events. When a user interacts with a widget (e.g., clicks a button), the widget emits a **Signal**. We connect that signal to a Python function, which is called a **Slot**.

## Guided Practice

Let's build a **Professional Greeter** app. The user types their name, clicks a button, and the app displays a personalized welcome message in a window.

*   **Step 1: Install PySide6**
    ```bash
    pip install PySide6
    ```

*   **Step 2: Create `greeter_app_example.py`**
    ```python
    import sys
    from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

    # This is our 'Slot' function
    def on_button_clicked():
        name = name_input.text()
        if name:
            result_label.setText(f"Hello, {name}! Welcome to PySide.")
        else:
            result_label.setText("Please enter your name!")

    # 1. Every PySide app needs a QApplication
    app = QApplication(sys.argv)

    # 2. Create the main Window
    window = QWidget()
    window.setWindowTitle("Greeting App")
    window.resize(300, 150)

    # 3. Create a Layout to hold our widgets
    layout = QVBoxLayout()

    # 4. Create and add Widgets
    name_input = QLineEdit()
    name_input.setPlaceholderText("Enter your name here...")
    
    greet_button = QPushButton("Greet Me!")
    # Connect the 'clicked' Signal to our 'on_button_clicked' Slot
    greet_button.clicked.connect(on_button_clicked) 

    result_label = QLabel("Waiting for input...")

    layout.addWidget(QLabel("What is your name?"))
    layout.addWidget(name_input)
    layout.addWidget(greet_button)
    layout.addWidget(result_label)

    # 5. Set the layout and show the window
    window.setLayout(layout)
    window.show()

    # 6. Start the Event Loop (this keeps the window open)
    sys.exit(app.exec())
    ```

## Checkpoints

* [ ] **The Click Counter**:
    Create an app with a button and a label. Every time the button is clicked, increment a number displayed on the label (Start at 0).
* [ ] **Color Changer**:
    Add three buttons: "Red", "Green", and "Blue". When a button is clicked, change the text color of a central label (Hint: use `label.setStyleSheet("color: red")`).
* [ ] **Unit Converter GUI**:
    Build a GUI with a text box for "Celsius" and a button. When clicked, calculate the Fahrenheit value and show it in a label.