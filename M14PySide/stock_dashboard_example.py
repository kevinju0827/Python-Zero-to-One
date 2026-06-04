"""Guided Practice — A dark-mode shop analytics dashboard.

Scenario: a small cafe-shop owner wants software that answers two needs.

  Page 1 — Overview (charts & KPIs):
    * What sold this month, broken down by product category?  (donut chart)
    * How did daily sales move across the month?               (line chart)
    * Which products actually made money?                      (cost/profit table)
  Page 2 — Records:
    * A sample of the stock-in / stock-out log.

To keep the focus on the GUI, all numbers are read once from a fixed
`shop_data.json` file — no database, no random generation. The two charts use
the built-in QtCharts module, so nothing here needs anything beyond PySide6.

Design notes: the look follows a modern dark "app" palette (Discord / PyCharm
Darcula family).
"""

import json
import os
import sys

from PySide6.QtCharts import (
    QAreaSeries,
    QChart,
    QChartView,
    QLineSeries,
    QPieSeries,
    QValueAxis,
)
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QColor, QPainter, QPalette, QPen
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

BG_APP = "#1e1f22"
BG_SIDEBAR = "#181a1d"
BG_CARD = "#2b2d31"
BG_ELEV = "#313338"
BORDER = "#3f4147"
TEXT = "#f2f3f5"
TEXT_MUTED = "#b5bac1"
TEXT_DIM = "#80848e"
ACCENT = "#5865f2"
GREEN = "#23a55a"
RED = "#f23f43"


# ===========================================================================
#  Data — one fixed JSON file, loaded once
# ===========================================================================
def load_data():
    """Read the pre-built sample numbers that drive every panel."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shop_data.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ===========================================================================
#  Manual entry dialog (display only — Save just closes the window)
# ===========================================================================
class MovementDialog(QDialog):
    """A small form that *shows* what an add-movement screen looks like.

    This is a UI demo: the Save button just closes the window. Wiring it to
    really store a row is left as a Checkpoint.
    """

    def __init__(self, product_names, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Movement")
        self.setMinimumWidth(320)

        form = QFormLayout(self)
        form.setContentsMargins(20, 20, 20, 16)
        form.setSpacing(12)

        self.product = QComboBox()
        self.product.addItems(product_names)

        self.kind = QComboBox()
        self.kind.addItem("Stock-in  (purchase)", "in")
        self.kind.addItem("Stock-out (sale)", "out")

        self.qty = QSpinBox()
        self.qty.setRange(1, 9999)
        self.qty.setValue(10)

        self.when = QDateEdit()
        self.when.setCalendarPopup(True)
        self.when.setDisplayFormat("yyyy-MM-dd")
        self.when.setDate(QDate(2026, 6, 15))

        form.addRow("Product:", self.product)
        form.addRow("Type:", self.kind)
        form.addRow("Quantity:", self.qty)
        form.addRow("Date:", self.when)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

        self.setStyleSheet(DIALOG_STYLE)


# ===========================================================================
#  Main window
# ===========================================================================
class Dashboard(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self._charts = []   # keep QChart refs alive (QChartView won't, in PySide)
        self.setWindowTitle("ShopBoard — Monthly Analytics")
        self.resize(1040, 720)
        self._build_ui()

    # --- layout ------------------------------------------------------------
    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        row = QHBoxLayout(root)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)
        row.addWidget(self._build_sidebar())

        # Two pages live in a QStackedWidget; the sidebar switches between them.
        self.stack = QStackedWidget()
        self.stack.addWidget(self._build_overview_page())   # index 0
        self.stack.addWidget(self._build_records_page())    # index 1
        row.addWidget(self.stack, stretch=1)

        self.setStyleSheet(STYLE)

    def _build_sidebar(self):
        bar = QFrame()
        bar.setObjectName("sidebar")
        bar.setFixedWidth(210)
        layout = QVBoxLayout(bar)
        layout.setContentsMargins(16, 20, 16, 16)
        layout.setSpacing(6)

        logo = QLabel("◆  ShopBoard")
        logo.setObjectName("logo")
        layout.addWidget(logo)
        layout.addSpacing(12)

        self.nav_overview = self._nav_button("Overview")
        self.nav_records = self._nav_button("Records")
        self.nav_overview.setChecked(True)
        self.nav_overview.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.nav_records.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        layout.addWidget(self.nav_overview)
        layout.addWidget(self.nav_records)

        layout.addStretch()

        add_btn = QPushButton("+  Add movement")
        add_btn.setObjectName("primary")
        add_btn.clicked.connect(self.add_movement)
        layout.addWidget(add_btn)

        footer = QLabel("JSON · PySide6")
        footer.setObjectName("footer")
        layout.addWidget(footer)
        return bar

    def _nav_button(self, text):
        btn = QPushButton(text)
        btn.setObjectName("nav")
        btn.setCheckable(True)
        btn.setAutoExclusive(True)   # only one nav item highlighted at a time
        return btn

    def _build_overview_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        title = QLabel("Overview")
        title.setObjectName("pageTitle")
        subtitle = QLabel(f"Sales & inventory · {self.data['month']}")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addLayout(self._build_kpis())
        layout.addLayout(self._build_charts(), stretch=1)
        layout.addWidget(self._build_table_card(), stretch=1)
        return page

    def _build_records_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        title = QLabel("Records")
        title.setObjectName("pageTitle")
        subtitle = QLabel("A sample of stock-in and stock-out movements")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        card = QFrame()
        card.setObjectName("card")
        box = QVBoxLayout(card)
        box.setContentsMargins(18, 14, 18, 16)
        headers = ["Date", "Product", "Category", "Type", "Qty", "Unit Value", "Total Value"]
        table = QTableWidget(len(self.data["records"]), len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setAlternatingRowColors(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for r, rec in enumerate(self.data["records"]):
            is_out = rec["kind"] == "out"
            type_text = "OUT · sale" if is_out else "IN · restock"
            type_color = GREEN if is_out else "#f0883e"
            cells = [
                (rec["date"], Qt.AlignLeft, None),
                (rec["name"], Qt.AlignLeft, None),
                (rec["category"], Qt.AlignLeft, None),
                (type_text, Qt.AlignLeft, type_color),
                (f"{rec['qty']:,}", Qt.AlignRight, None),
                (f"${rec['unit']:,.0f}", Qt.AlignRight, None),
                (f"${rec['total']:,.0f}", Qt.AlignRight, GREEN if is_out else RED),
            ]
            for c, (text, align, color) in enumerate(cells):
                item = QTableWidgetItem(text)
                item.setTextAlignment(align | Qt.AlignVCenter)
                if color:
                    item.setForeground(QColor(color))
                table.setItem(r, c, item)

        box.addWidget(table)
        layout.addWidget(card, stretch=1)
        return page

    def _build_kpis(self):
        row = QHBoxLayout()
        row.setSpacing(14)
        kpis = self.data["kpis"]
        self._add_kpi(row, "Revenue", f"${kpis['revenue']:,.0f}", ACCENT)
        self._add_kpi(row, "Profit", f"${kpis['profit']:,.0f}", GREEN)
        self._add_kpi(row, "Units Sold", f"{kpis['units']:,}", TEXT)
        self._add_kpi(row, "Margin", f"{kpis['margin']:.1f}%", "#f0b232")
        return row

    def _add_kpi(self, row, title, value_text, accent):
        card = QFrame()
        card.setObjectName("card")
        box = QVBoxLayout(card)
        box.setContentsMargins(18, 14, 18, 14)
        box.setSpacing(4)
        caption = QLabel(title)
        caption.setObjectName("kpiTitle")
        value = QLabel(value_text)
        value.setObjectName("kpiValue")
        value.setStyleSheet(f"color: {accent};")
        box.addWidget(caption)
        box.addWidget(value)
        row.addWidget(card)

    def _build_charts(self):
        row = QHBoxLayout()
        row.setSpacing(14)
        row.addWidget(self._chart_card("Sales by Category", self._donut_view()), stretch=1)
        row.addWidget(self._chart_card("Daily Units Sold", self._line_view()), stretch=1)
        return row

    def _chart_card(self, title, view):
        """Wrap a QChartView in the same dark #card frame as everything else."""
        card = QFrame()
        card.setObjectName("card")
        box = QVBoxLayout(card)
        box.setContentsMargins(18, 14, 18, 14)
        label = QLabel(title)
        label.setObjectName("cardTitle")
        box.addWidget(label)
        box.addWidget(view)
        return card

    def _donut_view(self):
        """A donut = a QPieSeries with a hole punched in the middle."""
        series = QPieSeries()
        series.setHoleSize(0.5)
        for c in self.data["categories"]:
            slice_ = series.append(f"{c['category']}  ({c['units']})", c["units"])
            slice_.setColor(QColor(c["color"]))
        chart = QChart()
        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignRight)
        self._style_chart(chart)
        return self._chart_view(chart)

    def _line_view(self):
        """A filled line chart: a QLineSeries wrapped in a QAreaSeries."""
        line = QLineSeries()
        for day, units in self.data["daily"]:
            line.append(day, units)

        self._charts.append(line)   # QAreaSeries won't keep its line series alive

        area = QAreaSeries(line)
        area.setColor(QColor(88, 101, 242, 130))      # translucent fill
        area.setPen(QPen(QColor(ACCENT), 2))          # solid top line

        chart = QChart()
        chart.addSeries(area)
        chart.legend().hide()

        axis_x = QValueAxis()
        axis_x.setLabelFormat("%d")
        axis_x.setTickCount(7)
        axis_y = QValueAxis()
        axis_y.setLabelFormat("%d")
        chart.addAxis(axis_x, Qt.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignLeft)
        area.attachAxis(axis_x)
        area.attachAxis(axis_y)
        for axis in (axis_x, axis_y):
            axis.setLabelsColor(QColor(TEXT_DIM))
            axis.setGridLineColor(QColor(BORDER))
            axis.setLinePenColor(QColor(BORDER))

        self._style_chart(chart)
        return self._chart_view(chart)

    def _style_chart(self, chart):
        """Make a chart blend into its dark #card frame."""
        chart.setBackgroundVisible(False)             # show the card behind it
        chart.legend().setLabelColor(QColor(TEXT_MUTED))

    def _chart_view(self, chart):
        self._charts.append(chart)   # hold a Python ref so the chart isn't GC'd
        view = QChartView(chart)
        view.setRenderHint(QPainter.Antialiasing)
        view.setMinimumHeight(240)
        return view

    def _build_table_card(self):
        card = QFrame()
        card.setObjectName("card")
        box = QVBoxLayout(card)
        box.setContentsMargins(18, 14, 18, 16)
        title = QLabel("Cost & Profit by Product")
        title.setObjectName("cardTitle")
        box.addWidget(title)

        headers = ["Product", "Category", "In Qty", "In Cost", "Sold", "Revenue", "Profit"]
        products = self.data["products"]
        table = QTableWidget(len(products), len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setAlternatingRowColors(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for r, row in enumerate(products):
            cells = [
                (row["name"], Qt.AlignLeft),
                (row["category"], Qt.AlignLeft),
                (f"{row['in_qty']:,}", Qt.AlignRight),
                (f"${row['in_cost']:,.0f}", Qt.AlignRight),
                (f"{row['out_qty']:,}", Qt.AlignRight),
                (f"${row['revenue']:,.0f}", Qt.AlignRight),
                (f"${row['profit']:,.0f}", Qt.AlignRight),
            ]
            for c, (text, align) in enumerate(cells):
                item = QTableWidgetItem(text)
                item.setTextAlignment(align | Qt.AlignVCenter)
                if c == 6:  # colour the profit column
                    item.setForeground(QColor(GREEN if row["profit"] >= 0 else RED))
                table.setItem(r, c, item)

        box.addWidget(table)
        return card

    # --- behaviour ---------------------------------------------------------
    def add_movement(self):
        """Open the entry form. This demo only *shows* the window."""
        product_names = [p["name"] for p in self.data["products"]]
        MovementDialog(product_names, self).exec()


STYLE = f"""
* {{ font-family: 'Segoe UI', 'Microsoft JhengHei', sans-serif; }}
QMainWindow, QWidget {{ background-color: {BG_APP}; color: {TEXT}; }}
/* Labels must be transparent — otherwise they paint the dark window colour
   and every title shows up sitting on a black strip inside its card. */
QLabel {{ background-color: transparent; }}

#sidebar {{ background-color: {BG_SIDEBAR}; border-right: 1px solid {BORDER}; }}
#logo {{ font-size: 16px; font-weight: 700; color: {TEXT}; }}
QPushButton#nav {{
    background-color: transparent; border: none; text-align: left;
    color: {TEXT_MUTED}; padding: 9px 10px; border-radius: 8px; font-weight: 600;
}}
QPushButton#nav:hover {{ background-color: {BG_CARD}; color: {TEXT}; }}
QPushButton#nav:checked {{ background-color: {BG_ELEV}; color: {TEXT}; }}
#footer {{ color: {TEXT_DIM}; font-size: 11px; }}

#pageTitle {{ font-size: 22px; font-weight: 700; }}
#pageSubtitle {{ color: {TEXT_MUTED}; font-size: 12px; }}

#card {{ background-color: {BG_CARD}; border: 1px solid {BORDER}; border-radius: 12px; }}
#cardTitle {{ font-size: 14px; font-weight: 700; color: {TEXT}; }}
#kpiTitle {{ font-size: 12px; color: {TEXT_DIM}; }}
#kpiValue {{ font-size: 24px; font-weight: 700; }}

QPushButton {{
    background-color: {BG_ELEV}; color: {TEXT}; border: 1px solid {BORDER};
    border-radius: 8px; padding: 8px 12px; font-weight: 600;
}}
QPushButton:hover {{ background-color: #3a3c42; }}
QPushButton#primary {{ background-color: {ACCENT}; border: none; color: white; }}
QPushButton#primary:hover {{ background-color: #4752c4; }}

QComboBox {{
    background-color: {BG_ELEV}; color: {TEXT}; border: 1px solid {BORDER};
    border-radius: 8px; padding: 6px 10px; min-width: 130px;
}}
QComboBox:hover {{ border-color: {ACCENT}; }}
QComboBox QAbstractItemView {{
    background-color: {BG_ELEV}; color: {TEXT};
    selection-background-color: {ACCENT}; outline: none;
}}

QTableWidget {{
    background-color: {BG_CARD}; alternate-background-color: {BG_ELEV};
    border: none; gridline-color: transparent; color: {TEXT};
}}
QTableWidget::item {{ padding: 6px; border: none; }}
QTableWidget::item:selected {{ background-color: rgba(88,101,242,0.30); }}
QHeaderView::section {{
    background-color: {BG_CARD}; color: {TEXT_DIM}; padding: 8px;
    border: none; border-bottom: 1px solid {BORDER}; font-weight: 600;
}}
QScrollBar:vertical {{ background: {BG_CARD}; width: 10px; margin: 0; }}
QScrollBar::handle:vertical {{ background: {BORDER}; border-radius: 5px; min-height: 24px; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; }}
"""


DIALOG_STYLE = f"""
QDialog {{ background-color: {BG_APP}; }}
QLabel {{ background: transparent; color: {TEXT_MUTED}; }}
QComboBox, QSpinBox, QDateEdit {{
    background-color: {BG_ELEV}; color: {TEXT};
    border: 1px solid {BORDER}; border-radius: 8px; padding: 6px 8px;
}}
QComboBox:hover, QSpinBox:hover, QDateEdit:hover {{ border-color: {ACCENT}; }}
QComboBox QAbstractItemView {{
    background-color: {BG_ELEV}; color: {TEXT};
    selection-background-color: {ACCENT};
}}
QPushButton {{
    background-color: {ACCENT}; color: white; border: none;
    border-radius: 8px; padding: 7px 16px; font-weight: 600;
}}
QPushButton:hover {{ background-color: #4752c4; }}
"""


def apply_dark_palette(app):
    """Make native dialogs match the dark theme too."""
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(BG_APP))
    palette.setColor(QPalette.WindowText, QColor(TEXT))
    palette.setColor(QPalette.Base, QColor(BG_CARD))
    palette.setColor(QPalette.AlternateBase, QColor(BG_ELEV))
    palette.setColor(QPalette.Text, QColor(TEXT))
    palette.setColor(QPalette.Button, QColor(BG_ELEV))
    palette.setColor(QPalette.ButtonText, QColor(TEXT))
    palette.setColor(QPalette.Highlight, QColor(ACCENT))
    palette.setColor(QPalette.HighlightedText, QColor("white"))
    app.setPalette(palette)


def main():
    data = load_data()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")     # consistent dark rendering on every OS
    apply_dark_palette(app)

    window = Dashboard(data)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
