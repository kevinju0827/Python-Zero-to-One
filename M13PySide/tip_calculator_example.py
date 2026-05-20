"""Guided Practice 1 — A tip calculator for a restaurant's back office.

Scenario: wait staff need a click-and-type tool to compute tips. A
terminal script would intimidate them; a small window will not.
"""

import sys

from PySide6.QtWidgets import (
    QApplication,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QWidget,
)


def compute_tip() -> None:
    """Slot: runs when the Calculate button is clicked."""
    raw = bill_input.text().strip()
    try:
        bill = float(raw)
    except ValueError:
        QMessageBox.warning(window, "Invalid input",
                            f"'{raw}' is not a number — please enter the bill in dollars.")
        return

    if bill < 0:
        QMessageBox.warning(window, "Invalid input", "Bill amount cannot be negative.")
        return

    percent = tip_input.value()
    tip = bill * percent / 100
    total = bill + tip

    # \n inside the label string becomes a real line break in QLabel.
    result_label.setText(f"Tip: ${tip:,.2f}\nTotal: ${total:,.2f}")


# 1. Every PySide app starts with a QApplication.
app = QApplication(sys.argv)

# 2. Build the window and its widgets.
window = QWidget()
window.setWindowTitle("Tip Calculator")
window.resize(320, 180)

bill_input = QLineEdit()
bill_input.setPlaceholderText("e.g. 42.50")

tip_input = QSpinBox()
tip_input.setRange(0, 30)
tip_input.setValue(15)
tip_input.setSuffix(" %")

calc_button = QPushButton("Calculate")
calc_button.clicked.connect(compute_tip)   # signal -> slot

result_label = QLabel("Enter a bill and press Calculate.")

# 3. QFormLayout gives us a tidy two-column "label : field" layout.
layout = QFormLayout()
layout.addRow("Bill amount ($):", bill_input)
layout.addRow("Tip percentage:",  tip_input)
layout.addRow(calc_button)
layout.addRow(result_label)
window.setLayout(layout)

# 4. Show the window and hand control to Qt's event loop.
window.show()
sys.exit(app.exec())
