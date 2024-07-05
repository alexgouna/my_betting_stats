import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget, QAbstractItemView, QLineEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QRegExp
import sqlite3
import Show_data.goal_stats_for_teams

class DesignDetailWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Details !!!")
        self.setGeometry(100, 100, 800, 400)

        # Setup the central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create the filter text box
        self.filter_box = QLineEdit()
        self.filter_box.setPlaceholderText("Filter")
        layout.addWidget(self.filter_box)

        # Create the QTreeView
        self.tree = QTreeView()
        self.tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.tree)

        # Setup the model
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            "ID", "Game_ID", "League", "Time", "Home", "Goal_Home", "Goal_Away", "Away", "Corner", "Corner_half",
            "Dangerous_Attacks", "Shots"
        ])

        # Setup the proxy model for filtering
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterKeyColumn(-1)  # Filter on all columns
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)  # Case insensitive filter
        self.tree.setModel(self.proxy_model)

        # Enable sorting
        self.tree.setSortingEnabled(True)
        self.tree.header().setSortIndicatorShown(True)
        self.tree.header().setSectionsClickable(True)
        self.tree.header().setDefaultAlignment(Qt.AlignCenter)

        # Populate the QTreeView
        self.populate_treeview()

        # Connect the double-click event
        self.tree.doubleClicked.connect(self.on_double_click)

        # Connect the filter box
        self.filter_box.textChanged.connect(self.filter_changed)

    def populate_treeview(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM table_team_games ORDER BY Time DESC')
        rows = c.fetchall()
        for row in rows:
            items = [QStandardItem(str(field)) for field in row]
            self.model.appendRow(items)
        conn.close()

    def on_double_click(self, index):
        item = self.proxy_model.mapToSource(index)
        my_game = [self.model.item(item.row(), col).text() for col in range(self.model.columnCount())]
        Show_data.goal_stats_for_teams.start(my_game[4], my_game[7])
        print(f"Selected ID: {my_game}")

    def filter_changed(self, text):
        reg_exp = QRegExp(text, Qt.CaseInsensitive, QRegExp.Wildcard)
        self.proxy_model.setFilterRegExp(reg_exp)
        print(f"Filter changed: {text}")  # Debugging print

def show_detailed_data():
    app = QApplication(sys.argv)
    window = DesignDetailWindow()
    window.show()
    app.exec_()

show_detailed_data()
