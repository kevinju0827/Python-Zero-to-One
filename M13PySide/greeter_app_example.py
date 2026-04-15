import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

def on_button_clicked():
    """This function is the 'Slot' that runs when the button is clicked."""
    name = name_input.text()
    if name:
        result_label.setText(f"Hello, {name}! Welcome to the GUI world.")
    else:
        result_label.setText("Please enter your name!")

# 1. Initialize the Application
# The sys.argv allows passing command-line arguments to the app
app = QApplication(sys.argv)

# 2. Create the main Window
window = QWidget()
window.setWindowTitle("Python Greeter App")
window.resize(400, 200)

# 3. Create a Vertical Layout
# This stacks widgets on top of each other
layout = QVBoxLayout()

# 4. Create UI Elements (Widgets)
title_label = QLabel("Welcome to the Python GUI Practice")
name_input = QLineEdit()
name_input.setPlaceholderText("Type your name here...")

greet_button = QPushButton("Send Greeting")
# Connect the 'clicked' signal of the button to our slot function
greet_button.clicked.connect(on_button_clicked)

result_label = QLabel("Status: Ready")

# 5. Add Widgets to the Layout
layout.addWidget(title_label)
layout.addWidget(name_input)
layout.addWidget(greet_button)
layout.addWidget(result_label)

# 6. Apply the Layout to the Window and Show it
window.setLayout(layout)
window.show()

# 7. Start the Event Loop
# This keeps the application running until the window is closed
sys.exit(app.exec())
